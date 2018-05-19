# coding:utf8
import os
from app import create_app, database
from app.models import Brick
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.environ.get("SOUCHA_CONFIG") or "local")
manager = Manager(app)
migrate = Migrate(app, database)


def make_shell_context():
    return dict(
        app=app,
        db=database,
        Brick=Brick
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
