"""A secure echo service, protected by ``auth_token``.

When the ``auth_token`` module authenticates a request, the echo service will
respond with all the environment variables presented to it by ``auth_token``.

"""
import json
import logging

from keystonemiddleware import auth_token


logging.basicConfig()


AUTH_TOKEN_CONF = {
    'auth_plugin': 'password',
    'auth_uri': 'http://{{ keystone_host | default(hostvars[groups["keystone"][0]]["ansible_default_ipv4"]["address"]) }}:35357/',
    'auth_url': 'http://{{ keystone_host | default(hostvars[groups["keystone"][0]]["ansible_default_ipv4"]["address"]) }}:35357/',
    'username': 'admin',
    'user_domain_id': 'default',
    'password': 'password',
    'project_name': 'admin',
    'project_domain_id': 'default',
    'memcached_servers': ['127.0.0.1:11211'],
    'token_cache_time': 300,
    'revocation_cache_time': 60,
    'memcache_security_strategy': 'ENCRYPT',
    'memcache_secret_key': '5bdc5pilx0o7re34z3yc2yt4x',
    'include_service_catalog': True}


def echo_app(environ, start_response):
    """A WSGI application that echoes the CGI environment to the user."""
    start_response('200 OK', [('Content-Type', 'application/json')])
    environment = dict((k, v) for k, v in environ.iteritems()
                       if k.startswith('HTTP_X_'))
    yield json.dumps(environment, indent=2)


application = auth_token.AuthProtocol(echo_app, AUTH_TOKEN_CONF)
