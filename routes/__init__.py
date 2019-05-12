import json
from jinja2 import PackageLoader, Environment
from models.session import Session
from models.user import User
from utils import log


def error(request):
    # body = JinjaTemplate.render('error.html')
    # return body
    return b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'


def redirect(url, session_id=None):
    """重定向至指定的url"""
    headers = {
        'Location': url,
    }
    if isinstance(session_id, str):
        headers.update({
            'Set-Cookie': 'session_id={}; path=/'.format(session_id)
        })
    r = formatted_headers(headers, 302)
    return r.encode()


def current_user(request):
    # log('<F_current_user s {}'.format(request.cookie))
    if 'session_id' in request.cookie:
        session_id = request.cookie['session_id']
        # log('<F_current_user s {}'.format(session_id))
        s = Session.one(session_id=session_id)
        # log('<F_current_user s {}'.format(s))
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.one(id=user_id)
            return u
    else:
        return User.guest()


def formatted_headers(headers, code=200):
    header = "HTTP/1.1 {} OK\r\n".format(code)
    header += ''.join([
        '{}: {}\r\n' .format(k, v) for k, v in headers.items()
    ])
    header += '\r\n'
    return header


def html_response(body, headers=None):
    h = {
        'Content-Type': 'text/html',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_headers(headers)
    r = header + body
    return r.encode()


def img_response(body, headers=None):
    h = {
        'Content-Type': 'image',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_headers(headers)
    r = header.encode() + body
    return r


def json_response(data, headers=None):
    h = {
        'Content-Type': 'application/json',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_headers(headers)
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode()


def initialized_environment():
    # fileLoader
    # path = os.path.join(os.path.dirname(__file__), 'templates')
    # loader = FileSystemLoader(path)
    # e = Environment(loader=loader)
    # return e

    # packageLoader
    env = Environment(loader=PackageLoader('resource', 'templates'))
    return env


class JinjaTemplate:
    # singleton pattern
    e = initialized_environment()

    @classmethod
    def render(cls, filename, **kwargs):
        template = cls.e.get_template(filename)
        return template.render(**kwargs)
