import time
import urllib


PAGE_403 = b"<html><body><h1><center>Error 403: Forbidden<center/></h1></body></html>"
PAGE_404 = b"<html><body><h1><center>Error 404: File not found<center/></h1></body></html>"

STATUSES = {
    200: 'OK',
    403: 'Forbidden',
    404: 'NOT_FOUND',
    405: 'METHOD_NOT_ALLOWED',
}


class HttpRequest(object):
    def __init__(self, data):
        self.message = data.split('\r\n')[0]
        self.data = data.split(' ')
        self.error = False
        self.method = self.get_method()
        self.query = ''
        self.url = self.get_url()

    def get_method(self):
        try:
            return self.data[0]
        except IndexError:
            self.error = True
            return ''

    def get_url(self):
        try:
            url = self.data[1]
        except IndexError:
            self.error = True
            return ''
        if url.rfind('?') is not -1:
            splitted_url = url.split('?')
            url = ''.join(splitted_url[:-1])
            self.query = splitted_url[-1]
        if url[-1] == "/" and url.rfind('.') is -1:
            url += "index.html"
        url = urllib.unquote(url).decode('utf8')
        return url

    def get_message(self):
        return self.message

    def is_have_error(self):
        return self.error


class HttpResponse(object):
    def __init__(self, request, root):
        self.request = request
        self.content_dir = root
        self.page_403 = PAGE_403
        self.page_404 = PAGE_404
        self.status_code = 200
        self.content_length = 0
        self.statuses = STATUSES
        self.methods = {
            'GET': self.get,
            'HEAD': self.head,
            'OPTIONS': self.options,
            'POST': self.not_allowed,
            'DELETE': self.not_allowed,
            'UPDATE': self.not_allowed,
            'PATCH': self.not_allowed,
            'TRACE': self.not_allowed,
            'PUT': self.not_allowed,
            'CONNECT': self.not_allowed,
        }
        self.content_types = {
            'html': 'text/html',
            'txt': 'text/plain',
            'css': 'text/css',
            'js': 'text/javascript',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'swf': 'application/x-shockwave-flash',
        }
        self.content_type = self._get_content_type()

    def get_response(self):
        return self.methods[self.request.method]()

    def get(self):
        return self._create_response()

    def head(self):
        return self._create_response(is_get=False)

    def options(self):
        header = 'HTTP/1.1 200 OK\r\n'
        header += 'Allow: OPTIONS, GET, HEAD\r\n'
        header += self._generate_last_headers()
        return header.encode()

    def not_allowed(self):
        header = 'HTTP/1.1 405 METHOD_NOT_ALLOWED\r\n'
        header += 'Allow: OPTIONS, GET, HEAD\r\n'
        header += self._generate_last_headers()
        return header.encode()

    def _create_response(self, is_get=True):
        body = self._generate_body()
        header = self._generate_headers()
        response = header.encode()
        if is_get:
            response += body
        return response

    def _is_valid(self):
        if self.request.url.find('/../../../') is not -1:
            return False
        else:
            return True

    def _get_content_type(self):
        file_type = self.request.url.split('.')[-1]
        content_type = self.content_types.get(file_type, 'application/octet-stream')
        return content_type

    def _generate_headers(self):
        header = 'HTTP/1.1 {0} {1}\r\n'.format(self.status_code, self.statuses[self.status_code])
        header += 'Content-Type: {0}\r\n'.format(self.content_type)
        header += self._generate_last_headers()
        return header

    def _generate_last_headers(self):
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header = 'Date: {now}\r\n'.format(now=time_now)
        header += 'Server: Otus teach http server\r\n'
        header += 'Content-Length: {0}\r\n'.format(self.content_length)
        header += 'Connection: close\r\n\r\n'
        return header

    def _generate_body(self):
        if self._is_valid():
            filepath = self.content_dir + self.request.url
            try:
                f = open(filepath, 'rb')
                response_data = f.read()
                f.close()
                status_code = 200
            except IOError as e:
                if filepath.endswith('index.html'):
                    status_code = 403
                    response_data = self.page_403
                else:
                    status_code = 404
                    response_data = self.page_404
        else:
            status_code = 403
            response_data = self.page_403
        content_length = len(response_data)
        self.content_length = content_length
        self.status_code = status_code
        return response_data
