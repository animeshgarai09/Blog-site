from flask import render_template, Blueprint, redirect, url_for, request, jsonify, abort
from flask_login import login_required, current_user
from project import db
from project.models import blogPost
from project.models import user as us
from project.core.picture_handler import addPicture
from project.user.forms import changeImage, changePassword
import string
import random
from werkzeug.security import generate_password_hash
import json
import os
from google.cloud import storage
import io

user = Blueprint('user', __name__)


@user.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    blog_posts = blogPost.query.order_by(
        blogPost.date.desc()).paginate(page, per_page=6)
    return render_template('dashboard.html', blog_posts=blog_posts)


@user.route('/transfer-data', methods=['POST'])
def transferData():
    print(request.get_json())
    if not os.path.exists('files'):
        os.makedirs('files')
    id = str(request.json['orgid'])
    # f = open("files/orgid-"+id+".txt", "w+")
    # f.write(json.dumps(request.get_json()))
    # f.close()

    storage_client = storage.Client.from_service_account_json('files\Blog-it-230426f278ca.json')
    bucket = storage_client.get_bucket('blog-it-282707.appspot.com')

    my_file = bucket.blob('files/orgid-'+id+'.txt')

    # create in memory file
    output = io.StringIO("This is a test \n This is a 2nd \n")
    # upload from string
    my_file.upload_from_string(output.read(), content_type="text/plain")

    output.close()
    return jsonify(data={'message':"Data recived with orgid "+ id})

@user.route('/search',methods=['GET'])
@login_required
def search():
    print(request.args.get('query'))
    blog_post=blogPost.query.whooshee_search('deploy').all()
    print(len(blog_post))
    return 'somthing'


@user.route('/profile/<name>/<int:id>',methods=['GET'])
@login_required
def profile(name,id):
    form=changeImage()
    password=changePassword()
    page=request.args.get('page',1,type=int)
    userDetails=us.query.get_or_404(id)
    blog_posts=blogPost.query.filter_by(author=userDetails).order_by(blogPost.date.desc()).paginate(page,per_page=6)
    return render_template('profile.html', pic=form,passForm=password,user=userDetails,blog_posts=blog_posts)

@user.route('/change-profile-image/<int:id>',methods=['POST'])
@login_required
def change_profile_image(id):
    form=changeImage()
    if current_user.id==id:
        if form.picture.data:
            print('in2')
            filename = (current_user.fullname+' '+str(current_user.id)).split(' ')
            filename = '_'.join(filename)
            letters = string.ascii_lowercase
            letters=''.join(random.choice(letters) for i in range(10))
            filename=filename+'_'+letters
            pic = addPicture(form.picture.data, filename, 'profile_pic')
            current_user.profile_image=pic
            db.session.commit()
            
            return jsonify(data={'link': url_for('static',filename='images/profile_pic/'+ pic)})
    abort(404)

@user.route('/change-password/<int:id>',methods=['POST'])
@login_required
def change_password(id):
    form=changePassword()
    if current_user.id==id:
        if form.validate_on_submit():
            users=us.query.filter_by(id=id).first()
            if users.checkPassword(form.oldPassword.data) and users is not None:
                users.hashPassword=generate_password_hash(form.newPassword.data)
                db.session.commit()
                return jsonify(data={'messeges': 'success'})
        abort(404)
    abort(404)
    


