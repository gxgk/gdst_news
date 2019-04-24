import sentry_sdk
import config
import logging
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from app.extensions import redis_store


def create_app():
    if config.DEBUG is False:
        sentry_logging = LoggingIntegration(
            level=logging.ERROR,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send no events from log messages
        )
        sentry_sdk.init(dsn=config.SENTRY_DSN, integrations=[FlaskIntegration(),
                                                             sentry_logging])

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config')

    redis_store.init_app(app)

    from app.school_news import school_news_mod
    app.register_blueprint(school_news_mod)

    return app
