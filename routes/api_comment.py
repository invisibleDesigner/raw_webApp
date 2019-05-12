from utils import log
from routes import json_response, current_user
from routes.permission import comment_owner_required, login_required
from models.comment import Comment


def add(request):
    form = request.json()
    u = current_user(request)
    form['user_id'] = u.id
    c = Comment.new(form)
    return json_response(c.json())


def delete(request):
    comment_id = int(request.query['comment_id'])
    Comment.delete(comment_id)
    d = dict(
        message="comment delete successful"
    )
    return json_response(d)


def update(request):
    form = request.json()
    comment_id = int(form['comment_id'])
    comment_content = form['content']
    log('<F update> comment_id', comment_id, type(comment_id))
    log('<F update> comment_content', comment_content, type(comment_content))
    c = Comment.one(id=comment_id)
    c.update(id=comment_id, content=comment_content)
    return json_response(c.json())


def route_dict():
    d = {
        '/api/comment/add': add,
        '/api/comment/delete': login_required(comment_owner_required(delete)),
        '/api/comment/update': login_required(comment_owner_required(update)),
    }
    return d
