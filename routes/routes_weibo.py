from models.user import User
from models.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    JinjaTemplate
)
from routes.permission import (
    login_required,
    same_user_required,
)


def weibo_index(request):
    """
    weibo 首页的路由函数
    """
    data = request.query
    if 'user_id' in data:
        u = User.one(id=int(data['user_id']))
    else:
        u = current_user(request)
    weibos = Weibo.all(user_id=u.id)
    body = JinjaTemplate.render('weibo_index_ajax.html', weibos=weibos, user=u)
    return html_response(body)


def weibo_add(request):
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user(request)
    form = request.form()
    Weibo.add(form, u.id)
    return redirect('/weibo/index')


def weibo_delete(request):
    weibo_id = int(request.query['weibo_id'])
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


def weibo_edit(request):
    weibo_id = int(request.query['weibo_id'])
    w = Weibo.one(id=weibo_id)
    body = JinjaTemplate.render('weibo_edit.html', weibo=w)
    return html_response(body)


def weibo_update(request):
    """
    用于增加新 weibo 的路由函数
    """
    form = request.form()
    Weibo.update(form)
    return redirect('/weibo/index')


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/weibo/add': login_required(weibo_add),
        '/weibo/delete': login_required(same_user_required(weibo_delete)),
        '/weibo/edit': login_required(same_user_required(weibo_edit)),
        '/weibo/update': login_required(same_user_required(weibo_update)),
        '/weibo/index': login_required(weibo_index),
    }
    return d
