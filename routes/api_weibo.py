from utils import log
from routes import json_response, current_user
from routes.permission import login_required, weibo_owner_required
from models.weibo import Weibo
from models.comment import Comment


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
def all(request):
    Weibos = Weibo.all()
    w = []
    for weibo in Weibos:
        c = {'comments': [comment.json() for comment in weibo.comments()]}
        log('F_weibo_all{}'.format(c))
        c['weibo'] = weibo.json()
        # w.append({weibo.id: c})
        w.append(c)

    # log('<F aip_weibo all> Weibos, comments', w)
    return json_response(w)


def add(request):
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json()
    # 创建一个 Weibo
    u = current_user(request)
    t = Weibo.add(form, u.id)
    # 把创建好的 Weibo 返回给浏览器
    return json_response(t.json())


def delete(request):
    log('<F weibo delete>')
    Weibo_id = int(request.query['weibo_id'])
    comments = Comment.all(weibo_id=Weibo_id)
    if len(comments) != 0:
        for comment in comments:
            comment.delete(comment.id)
    Weibo.delete(Weibo_id)

    d = dict(
        message="成功删除 Weibo"
    )
    return json_response(d)


def update(request):
    form: dict = request.json()
    Weibo_id = int(form.pop('weibo_id'))
    t = Weibo.update(Weibo_id, **form)
    return json_response(t.json())


def route_dict():
    d = {
        '/api/weibo/all': all,
        '/api/weibo/add': add,
        '/api/weibo/delete': login_required(weibo_owner_required(delete)),
        '/api/weibo/update': login_required(weibo_owner_required(update)),
    }
    return d
