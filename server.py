import socket
import threading

from models import SQLModel
from utils import log
from request import Request
from routes.routes_public import route_dict as public_routes
from routes.routes_user import route_dict as user_routes
from routes.routes_weibo import route_dict as weibo_routes
from routes.routes_weibo_comment import route_dict as comment_routes
from routes.api_weibo import route_dict as api_weibo_routes
from routes.api_comment import route_dict as api_comment_routes
from routes import error


def response_for_request(request):
    """routing distribution"""
    r = {}
    r.update(public_routes())
    r.update(user_routes())
    r.update(weibo_routes())
    r.update(comment_routes())
    r.update(api_weibo_routes())
    r.update(api_comment_routes())
    response = r.get(request.path, error)
    return response(request)


def get_all_request(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            return request.decode()


def process_request(connection):
    """对一个请求，用一个线程进行处理"""
    with connection:
        r = get_all_request(connection)

        log('此次请求的内容是:\n{}\n'.format(r))

        if len(r) > 0:
            request = Request(r)
            # log('<F_process_request_request:\n {}'.format(request))
            response = response_for_request(request)
            # log('<F_process_request_response:\n {}'.format(response))
            connection.sendall(response)
        else:
            connection.sendall(b'')
            log('接收到一个空请求')


def run(host, port):
    """start server"""
    SQLModel.init_db()
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(5)
        print("\n\n服务器已启动，地址为：http://localhost:{}\n\n".format(port))

        while True:
            connection, address = s.accept()
            log('ip:{}已连接\n'.format(address))
            threading.Thread(target=process_request, args=(connection,)).start()


if __name__ == '__main__':

    config = dict(
        host='0.0.0.0',
        port=5000,
    )

    run(**config)
