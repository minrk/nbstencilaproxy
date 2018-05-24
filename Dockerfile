FROM jupyter/r-notebook

# give NB_USER rights in the installation directory
ENV STENCILA_DIR /opt/stencila
USER root
RUN mkdir -p ${STENCILA_DIR} && chown -R ${NB_USER} ${STENCILA_DIR}

# install Stencila as NB_USER
USER ${NB_USER}
WORKDIR ${STENCILA_DIR}
ADD package.json package.json
RUN npm install
ADD stencila.js stencila.js
ADD stencila-host.js stencila-host.js
ADD index.html index.html
ADD app.js app.js

WORKDIR ${HOME}
ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt

USER ${NB_USER}
WORKDIR ${STENCILA_DIR}
ADD --chown=1000 . /tmp/jupyter-dar

# install Stencila using npm module
RUN npm install /tmp/jupyter-dar

# install Stencila proxy using Python module
RUN pip install /tmp/jupyter-dar
RUN jupyter serverextension enable --sys-prefix --py nbstencilaproxy
RUN jupyter nbextension install    --sys-prefix --py nbstencilaproxy
RUN jupyter nbextension enable     --sys-prefix --py nbstencilaproxy

# install Stencila R (ENV TAR is a fix for https://github.com/r-lib/devtools/issues/1722)
ENV TAR /bin/tar
ADD install.R install.R
RUN Rscript install.R

# add examples
ADD --chown=1000 archive/kitchen-sink ${HOME}/kitchen-sink
ADD --chown=1000 archive/py-jupyter ${HOME}/py-jupyter
ADD --chown=1000 archive/r-markdown ${HOME}/r-markdown
