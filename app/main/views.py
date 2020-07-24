from flask import render_template, request,redirect, url_for,abort
from . import main
from flask_login import login_required,current_user
from app.models import User, Post, Comment, MailList
from .forms import addPost, addComment,updatePost,updateProfile, mailListForm
from .. import db,photos
from ..request import get_quotes
from app.email import mail_message
from sqlalchemy import desc

@main.route('/',methods =['GET','POST'])
def index():
    '''
    View root page function that returns index page
    '''
    title = "my blog"
    quotes = get_quotes()
    quote = quotes['quote']
    author = quotes['author']

    form = mailListForm()
    if form.validate_on_submit():
        email = form.email.data
        new_mail = MailList(email = email)

        db.session.add(new_mail)
        db.session.commit()
        return redirect(url_for('main.index'))
    
    posts = Post.query.order_by(desc(Post.id)).all()
    return render_template('index.html', title = title, posts = posts, quote = quote ,author = author , form = form )


@main.route('/posts/<post_id>' ,methods = ['GET', 'POST'])
def post(post_id):
    '''
    View post page function that displays the posts in detail
    '''
    post = Post.query.filter_by(id = post_id).first()

    form = addComment()
    if form.validate_on_submit():
        content = form.content.data
        new_comment= Comment(content=content, post_id = post.id)
        new_comment.save_comment()
        return redirect(url_for('main.post', post_id = post.id))

    comments = Comment.get_comments(post.id)    


    return render_template('post.html', post = post, form =form ,comments = comments)


@main.route('/user/<uname>/addpost', methods = ['GET', 'POST'])
@login_required
def add_post(uname):
    title = "add post"
    form = addPost()
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        if "post_photo" in request.files:
            pic = photos.save(request.files["post_photo"])
            path =f"photos/{pic}"
            image_url = path

        new_post = Post(title = title, content = content, user = user, image_url = image_url)
        new_post.save_post()
        maillist = MailList.query.all()
        mails = []
        for mail in maillist:
            mails.append(mail.email)
        for mail in mails:
            mail_message("Update!","email/update", mail, user = current_user)

        return redirect(url_for('main.index'))

    return render_template('addpost.html', form = form, title = title )

@main.route('/update/<post_id>', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post_id = post.id

    if post is None:
        abort(404)

    form = updatePost()
    if form.validate_on_submit():
        post.content = form.content.data
        '''if "post_photo" in request.files:
            pic = photos.save(request.files["post_photo"])
            path =f"photos/{pic}"
            post.image_url = path'''

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('main.post' ,post_id = post_id))
    
    return render_template('updatepost.html', form = form)

@main.route('/deletecomment/<comment_id>')
@login_required
def delete_comment(comment_id):
    
    comment = Comment.query.filter_by(id = comment_id).first()
    post_id = comment.post_id
    print("-"*50
    )
    print(post_id)
   

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.post', post_id = post_id))

@main.route('/deletepost/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.index'))



@main.route('/user/<uname>')
def profile(uname):
    user = User. query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    return render_template("profile.html", user = user)

@main.route('/user/<uname>/update', methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)
    
    form = updateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.profile',uname = user.username))

    return render_template('updateprofile.html', form = form, user= user)

@main.route('/user/<uname>/update/pic', methods=['GET','POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_url = path
        db.session.commit()

    return redirect(url_for('main.profile', uname = uname))