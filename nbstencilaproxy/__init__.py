from nbstencilaproxy.handlers import setup_handlers

# Jupyter Extension points
def _jupyter_server_extension_paths():
    return [{
        'module': 'nbstencilaproxy',
    }]

def _jupyter_nbextension_paths():
    return [{
        "section": "tree",
        "dest": "nbstencilaproxy",
        "src": "static",
        "require": "nbstencilaproxy/tree"
    }]

def load_jupyter_server_extension(nbapp):
    setup_handlers(nbapp)
