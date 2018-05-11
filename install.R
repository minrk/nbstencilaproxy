library(devtools)
options(unzip = "internal")
# see https://github.com/stencila/r/blob/master/README.md
devtools::install_github("stencila/r")
stencila:::register()
# install.packages("tidyverse")
