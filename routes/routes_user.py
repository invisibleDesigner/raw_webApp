from urllib.parse import unquote_plus
from utils import log, random_string
from models.session import Session
from models.user import User
from routes import (
    html_response,
    redirect,
    current_user,
    JinjaTemplate,
)
from routes.permission import admin_required


def register_view(request):
    result = request.query.get('result', '')
    # log('<F_register_view_result', result)
    result = unquote_plus(result)
    body = JinjaTemplate.render('register.html', result=result)
    return html_response(body)


def register(request):
    # 根据传过来的信息，生成用户类
    form = request.form()
    u, result = User.register(form)
    return redirect('/user/register/view?result={}'.format(result))


def login(request):
    form = request.form()
    user, result = User.login(form)
    if not user.is_guest():
        session_id = Session.add(user_id=user.id)
        return redirect('/user/login/view?result={}'.format(result), session_id)
    else:
        return redirect('/user/login/view?result={}'.format(result))


def login_view(request):
    u = current_user(request)
    result = request.query.get('result', '')
    result = unquote_plus(result)
    body = JinjaTemplate.render('login.html', username=u.username, result=result)
    return html_response(body)


def user_view(request):
    users = User.find_all()
    # 下面这行生成一个 html 字符串
    users_html = """
            <h3>
                id:{},
                username:{},
                password:{}
            </h3>
            """
    users_html = ''.join([
        users_html.format(
            user.id, user.username, user.password
        ) for user in users
    ])
    log('<F user_view> users_html', users_html)
    return html_response('users.html', users=users_html)


def route_user(request):
    form = request.form()
    # 这里一定要转化，否则查不到
    user_id = int(form['id'])
    log('<F route_user_update> user_id', user_id)
    u = User.find_by(id=user_id)
    log('<F route_user_update> u', u)
    u.update(password=User.salted_password(form['password']))
    return redirect('/admin/users')


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/user/login': login,
        '/user/login/view': login_view,
        '/user/register': register,
        '/user/register/view': register_view,
    }
    return d
