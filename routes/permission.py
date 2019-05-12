from models.user import UserRole
from models.comment import Comment
from models.weibo import Weibo
from routes import (
    current_user,
    redirect,
    json_response,
)
from utils import log


def login_required(route_function):
    def wrapper(request):
        u = current_user(request)
        if u.is_guest():
            return redirect('/user/login/view')
        else:
            return route_function(request)
    return wrapper


def admin_required(route_function):
    def wrapper(request):
        user = current_user(request)
        if user.role == UserRole.admin:
            return route_function(request)
        else:
            return redirect('/user/login/view')
    return wrapper


def same_user_required(route_function):
    def wrapper(request):
        u = current_user(request)
        if 'weibo_id' in request.query:
            weibo_id = request.query['weibo_id']
        else:
            weibo_id = request.form()['weibo_id']
        w = Weibo.one(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')
    return wrapper


def weibo_or_comment_author_required(route_function):
    def wrapper(request):
        u = current_user(request)
        if 'weibo_id' in request.query and 'comment_id' in request.query:
            weibo_id = request.query['weibo_id']
            comment_id = request.query['comment_id']
        else:
            weibo_id = request.form()['weibo_id']
            comment_id = request.form()['comment_id']
        w = Weibo.one(id=int(weibo_id))
        c = Comment.find_by(id=int(comment_id))
        if w.user_id == u.id or c.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')
    return wrapper


def weibo_owner(request, u, weibo_id, route_function):
    log('<F weibo_owner route_function', route_function)
    w = Weibo.one(id=weibo_id)
    if w.user_id == u.id:

        return route_function(request)
    else:
        return json_response({'authority': 'f'})


def weibo_owner_required(route_function):
    def f(request):
        # log('weibo_owner_required')
        u = current_user(request)
        data_from_method = {
            'GET': request.query,
            'POST': request.json(),
        }
        weibo_id = int(data_from_method[request.method]['weibo_id'])
        log('<F weibo_owner_required route_function', route_function)
        return weibo_owner(request, u, weibo_id, route_function)
    return f


def comment_owner_required(route_function):
    def f(request):
        log('comment_owner_required')
        u = current_user(request)
        data_from_method = {
            'GET': request.query,
            'POST': request.json(),
        }
        comment_id = int(data_from_method[request.method]['comment_id'])
        # log('<F comment_owner_required weibo_id', comment_id)
        c = Comment.one(id=comment_id)
        w = Weibo.one(id=c.weibo_id)
        if w.user_id == u.id or c.user_id == u.id:
            return route_function(request)
        else:
            return json_response({'authority': 'f'})

    return f
