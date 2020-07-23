from flask import Flask
from flask_login import LoginManager

from .config import configs
from .handlers import blueprint_list


def register_extensions(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return 


def register_blueprints(app):
    for bp in blueprint_list:
        app.register_blueprint(bp)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    register_blueprints(app)
    register_extensions(app)

    return app
