import time
import urllib
import os

PAGE_400 = b"<html><body><h1><center>Error 400: Bad Request<center/></h1></body></html>"
PAGE_403 = b"<html><body><h1><center>Error 403: Forbidden<center/></h1></body></html>"
PAGE_404 = b"<html><body><h1><center>Error 404: File not found<center/></h1></body></html>"

STATUSES = {
    200: 'OK',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
}


class HttpRequest(object):
    def __init__(self, data):
        self.data = data.split(' ')
        self.error = False
        self.method = self.get_method()
        self.query = ''
        self.url = self.get_url()

        if data.find('\r\n') != -1:
            self.line_end = '\r\n'
        else:
            self.line_end = '\n'
        self.message = data.split(self.line_end)[0] or 'Bad Request'

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
        if url.rfind('?') != -1:
            splitted_url = url.split('?')
            url = ''.join(splitted_url[:-1])
            self.query = splitted_url[-1]
        if url[-1] == "/" and url.rfind('.') == -1:
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
        self.pages = {
            400: PAGE_400,
            403: PAGE_403,
            404: PAGE_404
        }
        self.content_length = 0
        self.filepath = root + request.url
        self.statuses = STATUSES
        self.status_code = self._get_status()
        self.methods = {
            'GET': self.get,
            'HEAD': self.head,
            'OPTIONS': self.options,
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
        return self.methods.get(self.request.method, self.not_allowed)()

    def get(self):
        return self._create_response()

    def head(self):
        return self._create_response(is_get=False)

    def options(self):
        header = 'HTTP/1.1 200 OK{end}'
        header += 'Allow: OPTIONS, GET, HEAD{end}'
        header += self._generate_last_headers()
        return header.format(end=self.request.line_end).encode()

    def not_allowed(self):
        header = 'HTTP/1.1 405 METHOD_NOT_ALLOWED{end}'
        header += 'Allow: OPTIONS, GET, HEAD{end}'
        header += self._generate_last_headers()
        return header.format(end=self.request.line_end).encode()

    def _create_response(self, is_get=True):
        body = self._generate_body()
        header = self._generate_headers()
        response = header.encode()
        if is_get:
            response += body
        return response

    def _is_valid(self):
        if self.request.url.find('/../../../') != -1:
            return False
        else:
            return True

    def _get_content_type(self):
        file_type = self.request.url.split('.')[-1]
        content_type = self.content_types.get(file_type, 'application/octet-stream')
        return content_type

    def _generate_headers(self):
        header = 'HTTP/1.1 {0} {1}{end}'.format(
            self.status_code,
            self.statuses[self.status_code],
            end=self.request.line_end
        )
        header += 'Content-Type: {0}{end}'.format(self.content_type, end=self.request.line_end)
        header += self._generate_last_headers()
        return header.format(end=self.request.line_end)

    def _generate_last_headers(self):
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header = 'Date: {now}{end}'.format(end=self.request.line_end, now=time_now)
        header += 'Server: Otus teach http server{end}'
        header += 'Content-Length: {0}{end}'.format(self.content_length, end=self.request.line_end)
        header += 'Connection: close{end}{end}'
        return header

    def _get_status(self):
        if self.request.is_have_error():
            status_code = 400
        elif self._is_valid():
            if os.path.isfile(self.filepath):
                status_code = 200
            else:
                if self.filepath.endswith('index.html'):
                    status_code = 403
                else:
                    status_code = 404
        else:
            status_code = 403
        return status_code

    def _generate_body(self):
        if self.status_code == 200:
            f = open(self.filepath, 'rb')
            response_data = f.read()
            f.close()
        else:
            response_data = self.pages[self.status_code]
        content_length = len(response_data)
        self.content_length = content_length
        return response_data
