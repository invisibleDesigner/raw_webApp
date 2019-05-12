var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiCommentAdd = function(form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weibo_id, callback) {
    var path = `/api/weibo/delete?weibo_id=${weibo_id}`
    ajax('GET', path, '', callback)
}

var apiCommentDelete = function(comment_id, callback) {
    var path = `/api/comment/delete?comment_id=${comment_id}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = `/api/weibo/update`
    ajax('POST', path, form, callback)
}

var apiCommentUpdate = function(form, callback) {
    var path = `/api/comment/update`
    ajax('POST', path, form, callback)
}

var weiboTemplate = function(weibo, comments) {
    var t = `
        <div class="weibo-cell" data-id="${weibo.id}">
            <span class="weibo-content">${weibo.content}</span>
            <button class="weibo-edit">edit</button>
            <button class="weibo-delete">delete</button>
            <div class="comment_list">
                ${comments}
                <br>
                <input class="comment-add-input">
                <button class="comment-add">add comment</button>
            </div>
        </div>
    `
    return t
}

var commentTemplate = function(comment) {
    var t = `
        <div class="comment-cell" data-id="${comment.id}">
            <span class="comment-content">${comment.content}</span>
            <button class="comment-edit">edit</button>
            <button class="comment-delete">delete</button>
        </div>
    `
    return t
}

var weiboUpdateTemplate = function(content) {
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${content}"/>
            <button class="weibo-update">update</button>
        </div>
    `
    return t
}

var commentUpdateTemplate = function(content) {
    var t = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${content}"/>
            <button class="comment-update">update</button>
        </div>
    `
    return t
}

var insertWeibo = function(weibo, comments) {
    var t_comments = ''
    for(var i = 0; i < comments.length; i++) {
        var comment = commentTemplate(comments[i])
        t_comments += comment
    }
    var weiboCell = weiboTemplate(weibo, t_comments)
    // log('<F inserWeibo weibo',  weibo)
    // log('<F inserWeibo weibo',  weiboCell)
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var insertWeiboUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}

var insertCommentUpdateForm = function(content, commentCell) {
    var updateForm = commentUpdateTemplate(content)
    commentCell.insertAdjacentHTML('beforeend', updateForm)
}

/* 加载全部微博的方法,js载入时，就会执行 */
var loadWeibos = function() {

    apiWeiboAll(function(weibos) {
        log('weibos', weibos)
        // log('weibos', weibos[0].weibo)
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i].weibo
            var comments = weibos[i].comments
            // log('weibo', weibo)
            insertWeibo(weibo, comments)
        }
    })
}

/* 增加一条微博的事件 */
var bindEventWeiboAdd = function() {
    var b = e('#id-button-weibo-add')
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(weibo) {
            insertWeibo(weibo, comments=[])
        })
    })
}

var bindEventCommentAdd = function() {
    var b = e('#id-weibo-list')
    b.addEventListener('click', function() {
        var self = event.target
        if (self.classList.contains('comment-add')) {
            var weiboCell = self.closest('.weibo-cell')
            var commentCell = e('.comment_list', weiboCell)
            var weiboId = weiboCell.dataset['id']
            var commentInput = e('.comment-add-input', weiboCell)
            var content = commentInput.value
            var form = {
                weibo_id: weiboId,
                content: content,
            }
            apiCommentAdd(form, function (comment) {
                c = commentTemplate(comment)
                commentCell.insertAdjacentHTML('afterbegin', c)
        })
    }
})}

var bindEventWeiboDelete = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('weibo-delete')) {
        var weiboId = self.parentElement.dataset['id']
        apiWeiboDelete(weiboId, function(form) {
            if (form.authority === 'f') {
                alert('no access')
            } else {
                self.parentElement.remove()
            }
        })
    }
})}

var bindEventCommentDelete = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('comment-delete')) {
        var commentCell = self.parentElement
        comment_id = commentCell.dataset['id']
        apiCommentDelete(comment_id, function(form) {
            if (form.authority === 'f') {
                alert('no access')
            } else {
                self.parentElement.remove()
            }
        })
    }
})}

/* 显示编辑组件 */
var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('weibo-edit')) {
        var weiboCell = self.closest('.weibo-cell')
        var weiboSpan = e('.weibo-content', weiboCell)
        var content = weiboSpan.innerText
        insertWeiboUpdateForm(content, weiboCell)
    }
    if (self.classList.contains('comment-edit')) {
        var commentCell = self.closest('.comment-cell')
        var commentSpan = e('.comment-content', commentCell)
        var ccontent = commentSpan.innerText
        insertCommentUpdateForm(ccontent, commentCell)
    }
})}

/* 更新微博数据 */
var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('weibo-update')) {
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var weiboInput = e('.weibo-update-input', weiboCell)
        var content = weiboInput.value
        var form = {
            weibo_id: weiboId,
            content: content,
        }
        apiWeiboUpdate(form, function(weibo) {
            if (weibo.authority === 'f') {
                alert('no access')
            } else {
                var weiboSpan = e('.weibo-content', weiboCell)
                weiboSpan.innerText = weibo.content
                var updateForm = e('.weibo-update-form', weiboCell)
                updateForm.remove()
            }
        })
    }
})}

/* 更新评论数据 */
var bindEventCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('comment-update')) {
        var commentCell = self.closest('.comment-cell')
        var commentId = commentCell.dataset['id']
        var commentInput = e('.comment-update-input', commentCell)
        var content = commentInput.value
        var form = {
            comment_id: commentId,
            content: content,
        }
        log('form', form)
        apiCommentUpdate(form, function(comment) {

            if (comment.authority === 'f') {
                alert('没有权限')
            } else {
                var commentSpan = e('.comment-content', commentCell)
                log('comment-content', comment.content)
                commentSpan.innerText = comment.content
                var updateForm = e('.comment-update-form', commentCell)
                updateForm.remove()
            }
        })
    }
})}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventCommentAdd()
    bindEventWeiboDelete()
    bindEventCommentDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()

