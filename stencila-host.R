# Get the port passed here from the `nbserverproxy.hanglers.SuperviseAndProxyHandler`
port <- as.integer(Sys.getenv("STENCILA_HOST_PORT"))
if (is.na(port)) port <- 2000

# Run the Stencila execution host without
# any authentication (handled by Jupyter)
Sys.setenv(STENCILA_AUTH = "false")

stencila::run(port=port)
