from flask_script import Manager, Server
from main import app, User, session, Base, Post,Comment,Tag
from config import DevConfig

manager = Manager(app)
manager.add_command('server', Server())

@manager.shell
def make_shell_context():
    return dict(
        app=app,
        User=User, 
        session=session, 
        Base=Base, 
        engine=DevConfig.engine, 
        Post=Post,
        Comment=Comment,
        Tag=Tag,
    )

if __name__ == '__main__':
    manager.run()