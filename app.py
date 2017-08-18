from gevent.monkey import patch_all

patch_all()

import os

from uplink_explorer.uplink_explorer import create_app
from uplink_explorer.config import config_path, config, ProdConfig


app = create_app(config_path)

if config == ProdConfig:
    from raven.contrib.flask import Sentry

    # XXX -- remove from open sourcing and put as env var
    sentry = Sentry(app, dsn='https://8590448340a54eb2a9c47b3628860560:23f589dd7412424ebee127f2a0114dd7@sentry.io/205685')


if __name__ == "__main__":
    app.run()
