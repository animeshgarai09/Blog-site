from flask import render_template, Blueprint, request, jsonify,abort,redirect,url_for
from flask_login import login_required, current_user
from project.blogpost.forms import createPost
from project import db
from project.models import blogPost
from project.core.picture_handler import addPicture

blogpost = Blueprint('blogpost', __name__)


@blogpost.route('/create-post', methods=['GET', 'POST'])
@login_required
def createpost():
    form = createPost()

    if request.method == 'POST':
        pic=None
        if form.picture.data:
            filename = (form.title.data+' '+current_user.fullname).split(' ')
            filename = '_'.join(filename)
            pic = addPicture(form.picture.data, filename, 'post_pic')

        post = blogPost(user_id=current_user.id,title=form.title.data,short=form.short.data,blog_image=pic,description=request.form.get('editordata'))
                        
        db.session.add(post)
        db.session.commit()
        return jsonify(data={'redirect': url_for('blogpost.blog_post',title=post.title,id=post.id)})
    return render_template('create-post.html', form=form)

@blogpost.route('/blog_post/<title>/update', methods=['GET', 'POST'])
@login_required
def update_post(title):
    blog_post=blogPost.query.get_or_404(request.args.get('id'))
    if title!=blog_post.title:
        abort(404)
    if blog_post.author.email!=current_user.email:
        abort(403)
    form = createPost()
    if request.method == 'POST':
        print("in")
        pic=None
        if form.picture.data:
            filename = (form.title.data+' '+current_user.fullname).split(' ')
            filename = '_'.join(filename)
            pic = addPicture(form.picture.data, filename, 'post_pic')
        
        blog_post.title=form.title.data
        blog_post.short=form.short.data
        if pic:
            blog_post.blog_image=pic
        blog_post.description=request.form.get('editordata')
                        
        db.session.add(blog_post)
        db.session.commit()
        return jsonify(data={'redirect': url_for('blogpost.blog_post',title=blog_post.title,id=blog_post.id)})
    else:
        form.title.data= blog_post.title
        form.short.data=blog_post.short
        return render_template('create-post.html', form=form,pic=blog_post.blog_image,title='update',code=blog_post.description,id=blog_post.id)

@blogpost.route('/blog_post/<title>/delete', methods=['GET'])
@login_required
def delete_post(title):
    blog_post=blogPost.query.get_or_404(request.args.get('id'))
    if title!=blog_post.title:
        abort(404)
    if blog_post.author.email!=current_user.email:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    return redirect(url_for('user.dashboard'))
    # if current_user.ema!=blog_post.title:
    #     abort(404)

@blogpost.route('/blog_post/<title>', methods=['GET'])
@login_required
def blog_post(title):
    blog_post=blogPost.query.get_or_404(request.args.get('id'))
    if title!=blog_post.title:
        abort(404)
    return render_template('blog_post.html', post=blog_post)
