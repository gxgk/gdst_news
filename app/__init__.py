from flask import Flask
from flask_redis import FlaskRedis
from raven.contrib.flask import Sentry
redis_store = FlaskRedis()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config')
    sentry = Sentry(app, dsn='https://9f470bbae23145b1b1ad402405ad310d:f7a19ed055d340508bdac85f71427b46@sentry.gxgk.cc/5')

    from app.school_news import school_news_mod
    app.register_blueprint(school_news_mod)
    redis_store.init_app(app)

    return app
