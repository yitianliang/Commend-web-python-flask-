from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from extension import db
from project import app
from models import User,Questions,Command

manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()
