import argparse
import logging
import multiprocessing
import os
import socket
import sys
from request_and_response import HttpRequest, HttpResponse
import multiprocessing.reduction as mp_reduction

DOCUMENT_ROOT = os.path.dirname(os.path.abspath(__file__))
WORKERS_COUNT = 4
HOST = '127.0.0.1'
PORT = 80
TIMEOUT = 10
PACKET_SIZE = 1024


def process_handle(queue, root):
    while True:
        handle = queue.get()
        fd = mp_reduction.rebuild_handle(handle)
        connection = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
        if connection == 'DONE':
            break
        data = ''
        try:
            data = connection.recv(PACKET_SIZE).decode()
        except:
            pass
        if not data:
            connection.close()
            continue
        request = HttpRequest(data)
        if request.is_have_error():
            logging.info('Bad request')
            connection.close()
            continue
        logging.info(request.get_message())
        resp = HttpResponse(request, root)
        connection.send(resp.get_response())
        connection.close()


class HTTPServer(object):

    def __init__(self, opts):
        self.host = opts.host
        self.port = opts.port
        self.root = opts.root
        self.timeout = opts.timeout
        self.workers_count = opts.workers_count
        self.queue = multiprocessing.Queue()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            logging.info("Start server")
            self.socket.bind((self.host, self.port))
        except (socket.gaierror, socket.error) as exc:
            logging.error("Error: Could not bind to port %s" % self.port)
            logging.debug(exc)
            self.shutdown()
        for i in range(self.workers_count):
            proccess = multiprocessing.Process(target=process_handle, args=((self.queue, self.root)))
            proccess.daemon = True
            proccess.start()
        self._listen()

    def shutdown(self):
        try:
            logging.info("Shutting down server")
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as exc:
            logging.error("Shutting down server error")
            logging.debug(exc)
        finally:
            sys.exit(1)

    def _listen(self):
        self.socket.listen(5)
        while True:
            (connection, address) = self.socket.accept()
            connection.settimeout(self.timeout)
            handle = mp_reduction.reduce_handle(connection.fileno())
            self.queue.put(handle)


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
