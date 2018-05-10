const path = require("path");
const darServer = require("dar-server");
const express = require("express");

const port = parseInt(process.env.STENCILA_PORT || '4000');
const archiveDir = process.env.STENCILA_DIR || process.env.HOME;

const server = express();

darServer.serve(server, {
  port: port,
  serverUrl: "http://localhost:" + port,
  rootDir: archiveDir,
  apiUrl: "/archives"
});

var staticDir = path.resolve(
  path.join(__dirname, "node_modules", "stencila", "dist")
);

console.log("Stencila app root: %s", staticDir);
console.log("DAR archive path: %s", archiveDir);
console.log("Serving stencila on :%s", port);

server.use("/", express.static(staticDir));
server.listen(port);
