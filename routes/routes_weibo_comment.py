from models.comment import Comment
from models.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    JinjaTemplate
)
from routes.permission import (
    login_required,
    weibo_or_comment_author_required
)


def comment_add(request):
    u = current_user(request)
    form = request.form()
    weibo = Weibo.find_by(id=int(form['weibo_id']))
    user_id = weibo.user_id
    c = Comment(form)
    c.user_id = u.id
    c.weibo_id = weibo.id
    c.save()
    return redirect('/weibo/index?user_id={}'.format(user_id))


def comment_edit(request):
    form = request.form()
    Comment.update(form)
    return redirect('/weibo/index')


def comment_edit_view(request):
    data = request.query
    comment_id = data['comment_id']
    body = JinjaTemplate.render('comment_edit.html', comment_id=comment_id)
    return html_response(body)


def comment_delete(request):
    data = request.query
    comment_id = int(data['comment_id'])
    Comment.delete(comment_id)
    return redirect('/weibo/index')


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/comment/add': login_required(comment_add),
        '/comment/edit': login_required(weibo_or_comment_author_required(comment_edit)),
        '/comment/edit/view': login_required(weibo_or_comment_author_required(comment_edit_view)),
        '/comment/delete': login_required(weibo_or_comment_author_required(comment_delete)),
    }
    return d
