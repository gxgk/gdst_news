from flask import Flask
from flask_redis import FlaskRedis

redis_store = FlaskRedis()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config')

    from app.school_news import school_news_mod
    app.register_blueprint(school_news_mod)
    redis_store.init_app(app)

    return app
