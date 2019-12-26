#!/usr/bin/env python
import gevent.monkey
gevent.monkey.patch_all()  # noqa

from pymaid.conf import settings
from pymaid.utils.logger import create_project_logger

settings.load_from_module('core.conf.settings')  # noqa
settings.load_from_root_path('shared.apps')  # noqa
settings.load_from_root_path('apps')  # noqa
create_project_logger('distributor-api')  # noqa


from core.app import create_app
import preload

server_conf = settings.namespaces['server']
# signals.auto_discover(server_conf['INSTALLED_APPS'])
app = create_app(server_conf['INSTALLED_APPS'])
# preload.preload()


if __name__ == '__main__':
    app.run(
        host=server_conf['DEBUG_HOST'], port=server_conf['DEBUG_PORT'],
        debug=server_conf['DEBUG'], threaded=True, use_reloader=False
    )
