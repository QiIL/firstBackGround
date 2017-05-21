from app import *
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Post,Comment,Tag
from app.config import DevConfig

manager = Manager(app)
manager.add_command('server', Server(debug=True), debug=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

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