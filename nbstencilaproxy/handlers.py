import pipes
import sys

from tornado import web
from urllib.parse import urlunparse, urlparse

from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler

from nbserverproxy.handlers import SuperviseAndProxyHandler

class AddSlashHandler(IPythonHandler):
    """Handler for adding trailing slash to URLs that need them"""
    @web.authenticated
    def get(self, *args):
        src = urlparse(self.request.uri)
        dest = src._replace(path=src.path + '/')
        self.redirect(urlunparse(dest))

# define our proxy handler for proxying the application

class StencilaProxyHandler(SuperviseAndProxyHandler):

    name = 'stencila'

    def get_env(self):
        return {
            'STENCILA_PORT': str(self.port),
            'STENCILA_ARCHIVE_DIR': self.state['notebook_dir'],
            'BASE_URL': self.state['base_url'],
        }

    def get_cmd(self):
        return [
            'sh', '-c', 'cd "$STENCILA_DIR"; node stencila.js',
        ]


class StencilaHostProxyHandler(SuperviseAndProxyHandler):

    name = 'stencila-host'

    def get_env(self):
        return {
            'STENCILA_HOST_PORT': str(self.port)
        }

    def get_cmd(self):
        return [
            'sh', '-c', 'cd "$STENCILA_DIR"; node stencila-host.js',
        ]


def setup_handlers(app):
    app.web_app.add_handlers('.*', [
        (
            app.base_url + 'stencila/(.*)',
            StencilaProxyHandler,
            dict(state=dict(
                base_url=app.base_url,
                notebook_dir=app.notebook_dir,
            )),

        ), (
            app.base_url + 'stencila-host/(.*)',
            StencilaHostProxyHandler,
            dict(state=dict(
                base_url=app.base_url,
                notebook_dir=app.notebook_dir,
            )),
        ),
    ])
