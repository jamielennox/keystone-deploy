"""A secure echo service, protected by ``auth_token``.

When the ``auth_token`` module authenticates a request, the echo service will
respond with all the environment variables presented to it by ``auth_token``.

"""
import json

from keystonemiddleware import auth_token

from oslo_log import log as logging
from oslo_config import cfg

CONF = cfg.CONF

logging.register_options(CONF)
logging.setup(CONF, 'echo')

LOG = logging.getLogger(__name__)


def echo_app(environ, start_response):
    """A WSGI application that echoes the CGI environment to the user."""
    start_response('200 OK', [('Content-Type', 'application/json')])
    environment = dict((k, v) for k, v in environ.iteritems()
                       if k.startswith('HTTP_X_'))
    yield json.dumps(environment, indent=2)


cfg.CONF(project='echo', default_config_files=['/etc/echo/echo.conf'])
cfg.CONF.log_opt_values(LOG, logging.DEBUG)

application = auth_token.AuthProtocol(echo_app, {})
