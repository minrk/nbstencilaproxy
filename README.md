# Jupyter + Stencila = `nbstencilaproxy`

[Jupyter](https://jupyter.org/) + [Dar](https://github.com/substance/dar) file format compatibility exploration for running [Stencila](http://stenci.la/) editor on [Binder](https://mybinder.org/)

[![PyPI version](https://badge.fury.io/py/nbstencilaproxy.svg)](https://badge.fury.io/py/nbstencilaproxy)

## Demo

Click on the button below to launch an online Jupyter instance on [mybinder.org](https://mybinder.org) based on this repository:

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/minrk/nbstencilaproxy/master?urlpath=stencila)

Open an the example Dar project by clicking on "New > Stencila Session":

![](new-session-button.png)

## About

This project is part of the [eLife  Innovation Sprint 2018](https://elifesci.org/innovationsprint2018) and [Mozilla Global Sprint 2018](https://mozilla.github.io/global-sprint/) (see [https://github.com/mozilla/global-sprint/issues/317](https://github.com/mozilla/global-sprint/issues/317))

The projects core module is a Python package, `nbstencilaproxy`, which is [available on PyPI](https://pypi.org/project/nbstencilaproxy/).
It is based on [`nbserverproxy`](https://github.com/jupyterhub/nbserverproxy) to run the services and the UI required to edit Stencila documents in the browser.
The concept is inspired by [`nbrsessionproxy`](https://github.com/jupyterhub/nbrsessionproxy).

`nbstencilaproxy` includes the following components:

- a JavaScript package for installing and running Stencila (client/UI and services) in a Jupyter container
- extension for the Jupyter UI to add a "New Stencila Session" button

## Team

- [@minrk](https://github.com/minrk)
- [@nuest](https://github.com/nuest)

## How does it work?

### The building blocks

Binder relies on [`repo2docker`](https://repo2docker.readthedocs.io/en/latest/) create a runtime environment from source code repositories.
`repo2docker` was extended as part of this project to detect Dar documents using the file `manifest.xml`, which is contained in all Dars.
If a `manifest.xml` is found, then `repo2docker` installs `nbstencilaproxy` into the image (see [code](https://github.com/jupyter/repo2docker/blob/master/repo2docker/buildpacks/base.py#L521)) and creates environment variables (`STENCILA_ARCHIVE_DIR` and `STENCILA_ARCHIVE`) to configure a single Dar document to be viewed in the Stencila UI.

The installation consists of the following steps and components:

1. Install [Stencila for Python](https://github.com/stencila/py) and/or Stencila for Python](https://github.com/stencila/py) from GitHub and register the package (thanks to the registration, the Stencila Host can find and connect these runtimes)
1. Install `nbstencilaproxy` itself, including a JavaScript module (see below for description of the npm; see `setup.py` for installation of the npm package as part of the Python module)
1. Install and enable the `nbstencilaproxy` **Jupyter notebook server extension**,  which serves the Stencila UI and services via proxies (see `nbstencilaproxy/handlers.py`)
1. Install and enable the `nbstencilaproxy` **Jupyter notebook extension**, which adds a menu item into the Jupyter UI to open Stencila (see `nbstencilaproxy/static/tree.js`)

### JavaScript module within `nbstencilaproxy`

The PyPI module includes a small [npm package](https://www.npmjs.com/) with JavaScript code, which serves the following purposes:

- pulls in Stencila' JavaScript depenencies, namely `stencila` and `stencila-host` (see `package.json`)
- includes code to run the `dar-server` and a static file server for the app using the files from the the module `stencila`s directory `dist` (see the file `stencila.js` for details)
- run a `stencila-host` on the port provided by nbserverproxy (see `stencila-host.js`)

This gives us control of the paths and let's us get rid of complex development features (e.g. `substance-bundler`).

The package includes [`stencila-node`](https://www.npmjs.com/package/stencila-node) as a dependency.
It provides the `JupyterContext` as well as a `NodeContext` (for executing Javascript) and a `SqliteContext` (for executing SQL).

We also made our own version of `app.js`, getting rid of the virtual file storage stuff (`vfs`), defaulting storage to `fs` (file system), because that is what is needed for Jupyter - we do not need to host any examples.
In the same line, we built own `index.html` (based on `example.html`) and serve that, which allows us to directly render a Dar document instead of a listing of examples and instruction and to use `app.js`.

Relevant _path configurations_ comprise (a) the local storage path and (b) the URLs used by the client, accessing the `dar-server` through `nbserverproxy`.

### Connecting Stencila to Jupyter kernels

Stencila has ["execution contexts"](https://stenci.la/learn/intro.html) (the equivalent of Jupyter's "kernels") for R, Python, SQL, JavaScript (Node.js), and Mini (Stencila's own simple language).
Execution contexts differ from kernels in a number of ways including local execution and dependency analysis of cells.
Both of these are necessary for the reactive, functional execution model of Stencila Articles and Sheets.

It is possible to install these execution contexts in the Docker image, and is done so for R
However, Stencila also has a `JupyterContext` which acts as a bridge between Stencila's API and Jupyter kernels.
Since the base image for BinderHub already has a Jupyter kernel for Python installed, it can always be used.
This does mean however, that some of the reactive aspects of the Stencila UI won't work as expected.
Also the `JupyterContext` is not well developed or tested.

## Install locally

If you have a local Jupyter instance, you can install the package directly:

```
pip install nbstencilaproxy
```

Enable the extensions for all users on the system:

```
jupyter serverextension enable  --py --sys-prefix nbstencilaproxy
jupyter nbextension     install --py --sys-prefix nbstencilaproxy
jupyter nbextension     enable  --py --sys-prefix nbstencilaproxy
```

## Run locally with `repo2docker`

You can run the latest release of `nbstencilaproxy` as part of `repo2docker`.

```bash
# install repo2docker: https://repo2docker.readthedocs.io/en/latest/usage.html#running-repo2docker-locally

# run repo2docker for a repository with Dar directories, e.g. archive/ in this repository (add '--no-build' option to only inspect Dockerfile)
repo2docker --debug ./archive
```

- Login by visiting the tokenized URL displayed e.g. `http://localhost:8888/?token=99a7bc13...`
- Click on the "New > Stencila Session" button on the Jupyter start page, opening the `py-jupyter` example, or
- Open one of the included examples by appending the following parameters to the URL:
  - Python (Jupyter Kernel): `?archive=py-jupyter`
  - R: `?archive=r-markdown`
  - Mini ([Stencila's own data analysis language](https://github.com/stencila/mini)): `?archive=kitchen-sink`

## Development

### Updating Stencila

The following places use/install Stencila components in specific versions:

- `repo2docker/buildpacks/base.py` installs github.com/stencila/py
- `repo2docker/buildpacks/r.py` installs github.com/stencila/r
- `nbstencilaproxy/package.json` installs [`stencila-node`](https://www.npmjs.com/package/stencila-node) and [`stencila`](https://www.npmjs.com/package/stencila) from npm

### Using local `nbstencilaproxy` in `repo2docker`

This is quite tricky to do, but useful to test the whole stack of tools.
It could be possible to copy the local files into the container, but a more practical approach is to temporarily telling `repo2docker` to install `nbstencilaproxy` from ones own fork.

In `repo2docker/buildpacks/base.py` find the line with

```bash
${NB_PYTHON_PREFIX}/bin/pip install --no-cache nbstencilaproxy==0.1.1 && \
```

which installs `nbstencilaproxy` from PyPI.
Replace it with the following line (using your username for `<user>`)

```bash
${NB_PYTHON_PREFIX}/bin/pip install https://github.com/<user>/nbstencilaproxy/archive/master.tar.gz && \
```

## License

BSD 3-Clause License
