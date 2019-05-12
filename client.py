import socket
import ssl

from utils import log


def parsed_url(url):
    """解析url,获得协议，主机，端口，资源地址"""

    # 解析出协议
    separator = '://'
    i = url.find('://')
    if i == -1:
        protocol = 'http'
        u = url
    else:
        protocol = url[:i]
        u = url[i + len(separator):]

    # 解析出资源路径
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 解析出主机和端口
    i = host.find(':')
    if i == -1:
        port_dict = dict(
            http=80,
            https=443,
        )
        port = port_dict[protocol]
    else:
        h = host.split(':', 1)
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def parsed_response(r):
    """解析出：状态码， headers, body"""
    header, body = r.split('\r\n', 1)
    header_list = header.split('\r\n')

    # 返回值得形式为：HTTP/1.1 200 OK\r\n
    status_code = int(header_list[0].split()[1])

    headers = {}
    for line in header_list[1:]:
        k, v = line.split(': ', 1)
        headers[k] = v

    return status_code, headers, body


def response_by_socket(s):
    """接收socket的返回值"""
    response = b''
    buffer_size = 1000
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            return response.decode()


def socket_by_protocol(protocol):
    """根据协议建立不同类型的链接"""
    s = socket.socket()
    if protocol == 'https':
        return ssl.wrap_socket(s)
    else:
        return s


def get(url):
    protocol, host, port, path = parsed_url(url)

    s = socket_by_protocol(protocol)
    s.connect((host, port))
    request = "GET {} HTTP/1.1\r\n\r\n".format(path)
    s.send(request.encode())
    response = response_by_socket(s)
    log('<F get> response', response)
    status_code, headers, body = parsed_response(response)

    if status_code == 301:
        url = headers['Location']
        return get(url)
    else:
        return response, status_code


def main():
    url = "http://localhost:3001"
    response, status_code = get(url)
    print(response)


if __name__ == '__main__':
    main()
