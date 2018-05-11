library(devtools)
options(unzip = "internal")
# see https://github.com/stencila/r/blob/master/README.md
#devtools::install_github("stencila/r")
# https://github.com/stencila/r/issues/21
devtools::install_github("nuest/r")
stencila:::install()
# install.packages("tidyverse")
