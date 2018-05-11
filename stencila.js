const path = require("path");
const darServer = require("dar-server");
const express = require("express");

const port = parseInt(process.env.STENCILA_PORT || '4000');
const archiveDir = process.env.STENCILA_ARCHIVE_DIR || process.env.HOME;
const baseUrl = process.env.BASE_URL || "/";
const serverUrl = baseUrl + "stencila";
const server = express();

darServer.serve(server, {
  port: port,
  serverUrl: serverUrl,
  rootDir: archiveDir,
  apiUrl: "/archives"
});

node_modules = path.dirname(path.dirname(path.resolve(__dirname)));
stencilaDist = path.join(node_modules, "stencila", "dist");

console.log("Stencila app root: %s", stencilaDist);
console.log("DAR archive path: %s", archiveDir);
console.log("DAR public URL: %s", serverUrl);
console.log("Serving stencila on :%s", port);

server.use("/stencilaDist", express.static(stencilaDist));
server.use("/", express.static(__dirname));
server.listen(port);
