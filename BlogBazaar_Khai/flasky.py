import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import Comment, User, Role, Permission, Follow
import monkey_patch

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.before_first_request
def before_first_request():
    # Thêm quyền vào cơ sở dữ liệu khi ứng dụng khởi động
    Role.insert_roles()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, Follow=Follow, Comment=Comment)

# print("SECRET_KEY = " + app.config["SECRET_KEY"])
# print("MAIL_SERVER = " + app.config['MAIL_SERVER'])
# print("MAIL_PORT = " + str(app.config['MAIL_PORT']))
# print("MAIL_USERNAME = " + app.config['MAIL_USERNAME'])
# print("MAIL_PASSWORD = " + app.config['MAIL_PASSWORD'])
# print("FLASKY_MAIL_SUBJECT_PREFIX = " + app.config['FLASKY_MAIL_SUBJECT_PREFIX'])
# print("FLASKY_MAIL_SENDER = " + app.config['FLASKY_MAIL_SENDER'])
# print("FLASKY_ADMIN = " + app.config['FLASKY_ADMIN'])
# print("FLASKY_POSTS_PER_PAGE = " + app.config['FLASKY_POSTS_PER_PAGE'])


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
