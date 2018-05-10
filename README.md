# jupyter-dar

[Jupyter](https://jupyter.org/) + [DAR](https://github.com/substance/dar) compatibility exploration for running [Stencila](http://stenci.la/) on [binder](https://mybinder.org/)

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/minrk/jupyter-dar/master?urlpath=%2Fstencila%2F)

This project is part of the [eLife  Innovation Sprint 2018](https://elifesci.org/innovationsprint2018) and [Mozilla Global Sprint 2018](https://mozilla.github.io/global-sprint/) (see [https://github.com/mozilla/global-sprint/issues/317](https://github.com/mozilla/global-sprint/issues/317))

## Team

- [@minrk](https://github.com/minrk)
- [@nuest](https://github.com/nuest)

## How?

### Running Stencila in the Jupyter container

We first used Stencila's development build to run the app using `node make -w -s -d /our/own/dir`, but struggled a bit to configure the file storage, i.e. the `dar-server`, to use the directory we want to, and to run it in a full path configured by us instead of `make.js` starting the `dar-server` relative to `__dirname`.
_Eventually_ we ended up implementing our own minimal npm package that pulls in Stencila as a dependency and runs the `dar-server` and static file server for the app using the files from the `dist` directory.
See the file `stencila.js` for details.
This gives us control of the paths and let's us get rid of complex development features (`substance-bundler` etc.).

We also made our own version of `app.js`, getting rid of the virtual file storage stuff (`vfs`), defaulting storage to `fs` (file system), because that is what is needed for Jupyter - we do not need to host any examples.
In the same line, we built own `index.html` (based on `example.html`) and serve that, which allows us to directly render a DAR document instead of a listing of examples and instruction and to use our `app.js`.

Relevant path configurations comprise the local storage path _as well as_ the URLs used by the client, accessing the `dar-server` through the `nbserverproxy`.

The `Dockerfile` installs our helper npm package and adds + configures the `nbserverproxy` tool (see `requirements.txt` and `jupyter_notebook_config.py`).

## License

BSD 3-Clause License
