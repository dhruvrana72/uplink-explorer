from gevent.monkey import patch_all

patch_all()

import os

from uplink_explorer.uplink_explorer import create_app
from uplink_explorer.config import config_path, config, ProdConfig

app = create_app(config_path)

if config == ProdConfig and os.environ.get('SENTRY'):
    from uplink_explorer.extensions import sentry

    sentry.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
