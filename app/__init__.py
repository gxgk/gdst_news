from flask import Flask
from flask_redis import FlaskRedis
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import config

redis_store = FlaskRedis()


def create_app():
    if config.DEBUG is False:
        sentry_sdk.init(dsn=config.SENTRY_DSN,integrations=[FlaskIntegration()])

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config')

    from app.school_news import school_news_mod
    app.register_blueprint(school_news_mod)
    redis_store.init_app(app)

    return app
