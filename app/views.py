from app import app
from flask import render_template
from app import session
import models
from models import *
from forms import *
import datetime


def sider_render():
    recent = session.query(Post)
  
@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    posts = session.query(Post).order_by(
        Post.publish_date.desc()
    )

    return render_template(
        'home.html',
        posts = posts
    )

@app.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data 
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()
        session.add(new_comment)
    session.commit()
    post = session.query(Post).get(post_id)
    tags = post.tag
    comments = session.query(Comment).filter_by(post_id=post.id).order_by(Comment.date.desc()).all()
    
    return render_template(
        'post.html',
        post = post,
        tags = tags,
        comments = comments,
        form = form
    )

@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = session.query(Tag).filter_by(title=tag_name).first()
    print tag, '+++++++++++++++++++++++++++++++++++++++++'
    posts = session.query(Post).join(Post.tag).filter_by(title=tag.title).order_by(Post.publish_date.desc()).all()
    return render_template(
        'tag.html',
        tag = tag,
        posts = posts
    )

@app.route('/user/<string:username>')
def user(username):
    user = session.query(User).filter_by(username=username).first()
    posts = session.query(Post).filter_by(user_id=user.id).order_by(Post.publish_date.desc()).all()

    return render_template(
        'user.html',
        user = user,
        posts = posts
    )
if __name__ == '__main__':
    app.run()