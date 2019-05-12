import json
from utils import log


class Request(object):

    def __init__(self, r):
        self.raw_data = r
        self.header = {}
        self.body = ''

        self.method = ''
        self.path = ''
        self.query = {}
        self.cookie = {}

        self.http_separator = {'line': '\r\n', 'head_body': '\r\n\r\n'}

        self.parsed_raw_data()
        self.add_cookies()

    def add_cookies(self):
        if 'Cookie' in self.header:
            key, value = self.header['Cookie'].split('=', 1)
            self.cookie[key] = value

    def parsed_raw_data(self):
        """
        head and body separator by \r\n\r\n, request_line and header separator by \r\n
        """
        head, self.body = self.raw_data.split(self.http_separator['head_body'], 1)
        # no header condition
        if self.http_separator['line'] in head:
            request_line, header = head.split(self.http_separator['line'], 1)
            self.parsed_header(header)
        else:
            request_line = head
            self.header = {}
        self.parsed_request_line(request_line)

    def parsed_header(self, header):
        header_list = header.split(self.http_separator['line'])
        for header in header_list:
            key, value = header.split(': ', 1)
            self.header[key] = value

    def parsed_request_line(self, request_line):
        parts = request_line.split()
        self.method, query_path = parts[0], parts[1]
        self.parsed_query_path(query_path)

    def parsed_query_path(self, query_path):
        """
        just like
        input '/baidu?keyword=haa'
        output
            path /gua
            query {
            'keyword': 'haa'
            }
        """
        e = query_path.find('?')
        if e == -1:
            self.path = query_path
            self.query = {}
        else:

            query_string = query_path[e+1:]
            args = query_string.split('&')
            query = {}
            for arg in args:
                key, value = arg.split('=')
                query[key] = value

            self.path = query_path[:e]
            self.query = query

    def form(self):
        """parse body to dict"""
        args = self.body.split('&')
        f = {}
        for arg in args:
            key, value = arg.split('=')
            f[key] = value
        return f

    def json(self):
        """
        把 body 中的 json 格式字符串解析成 dict 或者 list 并返回
        """
        # log('<F json>', len(self.body))
        if len(self.body) != 0:
            return json.loads(self.body)

