import argparse
import logging
import os
import socket
import sys
from request_and_response import HttpRequest, HttpResponse
import threading
from Queue import Queue

DOCUMENT_ROOT = os.path.dirname(os.path.abspath(__file__))
WORKERS_COUNT = 4
HOST = '127.0.0.1'
PORT = 8080
TIMEOUT = 10
PACKET_SIZE = 1024
MAX_PACKET_SIZE = 8192


def worker_handle(sock, root, timeout):
    while True:
        (connection, address) = sock.accept()
        connection.settimeout(timeout)

        data = _receive(connection)
        request = HttpRequest(data)
        logging.info(request.get_message())
        resp = HttpResponse(request, root)
        connection.sendall(resp.get_response())
        connection.close()


def _receive(connection):
    buffer = ''
    buffer_size = 0
    while True:
        try:
            data = connection.recv(PACKET_SIZE)
            if buffer_size > MAX_PACKET_SIZE:
                break
            if data:
                buffer += data.decode()
                buffer_size += len(data)
            else:
                break
            if buffer.endswith('\r\n\r\n') or buffer.endswith('\n\n'):
                break
        except socket.timeout:
            break
    return buffer


class HTTPServer(object):
    def __init__(self, opts):
        self.host = opts.host
        self.port = opts.port
        self.root = opts.root
        self.timeout = opts.timeout
        self.workers_count = opts.workers_count
        self.queue = Queue()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        logging.info("Start server")
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        for i in range(self.workers_count):
            t = threading.Thread(target=worker_handle, args=(self.socket, self.root, self.timeout))
            t.setDaemon(True)
            t.start()
        worker_handle(self.socket, self.root, self.timeout)

    def shutdown(self):
        try:
            logging.info("Shutting down server")
            self.socket.close()
        except Exception as exc:
            logging.error("Shutting down server error")
            logging.debug(exc)
        finally:
            sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root", default=DOCUMENT_ROOT, help="documents path")
    parser.add_argument("-w", "--workers_count", default=WORKERS_COUNT, help="count of workers", type=int)
    parser.add_argument("-a", "--host", default=HOST, help="host address")
    parser.add_argument("-p", "--port", default=PORT, help="port for connection", type=int)
    parser.add_argument("-t", "--timeout", default=TIMEOUT, help="timeout for connection", type=int)
    parser.add_argument("-l", "--log", default=None, help='log file path')
    parser.add_argument("-d", "--debug", default=False, help='debug logging', action="store_true")
    opts = parser.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO if not opts.debug else logging.DEBUG,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')

    demon = HTTPServer(opts)
    try:
        demon.start()
    except KeyboardInterrupt:
        logging.info('Program exit')
    except Exception as e:
        logging.exception("Unexpected error: %s" % e)
        sys.exit(1)
    finally:
        demon.shutdown()

