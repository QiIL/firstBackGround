from flask import Flask, render_template
from config import DevConfig
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy  import Column,Integer,String,Text,ForeignKey,DateTime,Table
from sqlalchemy import func
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config.from_object(DevConfig)
Base = declarative_base()
session = DevConfig.Session()

post_tag = Table('post_tag', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base): #parent
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    #relationship
    post = relationship("Post", back_populates='user')
    
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<User, id = '%d', username='%s', password='%s'>" % (
            self.id, self.username, self.password)

class Post(Base): #children
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    text = Column(Text())
    publish_date = Column(DateTime)
    #relationship
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates='post')
    comment = relationship("Comment", back_populates='post')
    tag = relationship("Tag", secondary=post_tag, back_populates='post')

    def __init__(self, title):
        self.title = title
    
    def __repr__(self):
        return "<Post '{}'>".format(self.title)

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    text = Column(Text())
    date = Column(DateTime())
    #relationship
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", back_populates='comment')
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Comment '{}'".format(self.text[:15])

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    post = relationship("Post", secondary=post_tag, back_populates='tag')

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Tag '{}>".format(self.title)

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

@app.route('/post/<int:post_id>')
def post(post_id):
    post = session.query(Post).get(post_id)
    tags = post.tag
    comments = session.query(Comment).filter_by(post_id=post.id).order_by(Comment.date.desc()).all()
    
    return render_template(
        'post.html',
        post = post,
        tags = tags,
        comments = comments
    )

@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = session.query(Tag).filter_by(title=tag_name).first()
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