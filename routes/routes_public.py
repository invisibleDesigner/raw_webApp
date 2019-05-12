from routes import (
    current_user,
    JinjaTemplate,
    html_response,
    img_response,
)


def index(request):
    u = current_user(request)
    body = JinjaTemplate.render('index.html', username=u.username)
    return html_response(body)


def static(request):
    filename = request.query['file']
    path = 'resource/static/' + filename
    with open(path, 'rb') as f:
        # header = b'HTTP/1.x 200 OK\r\n\r\n'
        # img = header + f.read()
        # return img
        return img_response(f.read())


def route_dict():
    d = {
        '/': index,
        '/static': static,
    }
    return d
