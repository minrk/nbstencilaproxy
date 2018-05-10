import pipes
import sys

from nbserverproxy.handlers import SuperviseAndProxyHandler

# define our proxy handler for proxying the application

class StencilaProxyHandler(SuperviseAndProxyHandler):

    name = 'stencila'

    def get_env(self):
        return {
            'STENCILA_PORT': str(self.port),
            'STENCILA_ARCHIVE_DIR': self.state['notebook_dir'],
        }

    def get_cmd(self):
        return [
            'sh', '-c', 'cd "$STENCILA_DIR"; node stencila.js',
        ]


def add_handlers(app):
    app.web_app.add_handlers('.*', [
        (
            app.base_url + 'stencila/(.*)',
            StencilaProxyHandler,
            dict(state=dict(
                notebook_dir=app.notebook_dir,
            )),
        ),
    ])


# fake a module to load the proxy handler as an extension
module_name = '_myproxymod'
import types
mod = types.ModuleType(module_name)
sys.modules[module_name] = mod
mod.load_jupyter_server_extension = add_handlers
c.NotebookApp.nbserver_extensions.update({
    module_name: True,
})
