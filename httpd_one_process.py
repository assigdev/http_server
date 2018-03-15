import argparse
import logging
import multiprocessing
import os
import socket
import sys
from request_and_response import HttpRequest, HttpResponse

DOCUMENT_ROOT = os.path.dirname(os.path.abspath(__file__))
HOST = '127.0.0.1'
PORT = 80
TIMEOUT = 60
PACKET_SIZE = 1024


class HTTPServer(object):

    def __init__(self, opts):
        self.host = opts.host
        self.port = opts.port
        self.root = opts.root
        self.timeout = opts.timeout
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            logging.info("Start server")
            self.socket.bind((self.host, self.port))
        except socket.gaierror as exc:
            logging.exception("Error: Could not bind to port %s" % self.port)
            logging.debug(exc)
            self.shutdown()
        self._listen()

    def shutdown(self):
        try:
            logging.info("Shutting down server")
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as exc:
            logging.exception("Shutting down server error")
            logging.debug(exc)
        finally:
            sys.exit(1)

    def _listen(self):
        self.socket.listen(5)
        while True:
            (connection, address) = self.socket.accept()
            connection.settimeout(self.timeout)
            self._handle_client(connection)

    def _handle_client(self, connection):
        data = connection.recv(PACKET_SIZE).decode()
        if not data:
            return
        request = HttpRequest(data)
        logging.info(request.get_message())
        resp = HttpResponse(request, self.root)
        connection.send(resp.get_response())
        connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root", default=DOCUMENT_ROOT, help="documents path")
    parser.add_argument("-a", "--host", default=HOST, help="host address")
    parser.add_argument("-p", "--port", default=PORT, help="port for connection", type=int)
    parser.add_argument("-t", "--timeout", default=TIMEOUT, help="timeout for connection", type=int)
    parser.add_argument("-l", "--log", default=None, help='log file path')
    parser.add_argument("-d", "--debug", default=False, help='debug logging', action="store_true")
    opts = parser.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO if not opts.debug else logging.DEBUG,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')

    try:
        demon = HTTPServer(opts)
        demon.start()
    except KeyboardInterrupt:
        logging.info('Program exit')
    except Exception as e:
        logging.exception("Unexpected error: %s" % e)
        sys.exit(1)
    finally:
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
