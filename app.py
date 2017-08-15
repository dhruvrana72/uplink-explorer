from gevent.monkey import patch_all

patch_all()

import os

from uplink_explorer.uplink_explorer import create_app
from uplink_explorer.config import config_path


app = create_app(config_path)


if __name__ == "__main__":
    app.run()
