const path = require("path");
const fs = require("fs");
const darServer = require("dar-server");
const express = require("express");
const logging = require("morgan");
const mustache = require("mustache");

const port = parseInt(process.env.STENCILA_PORT || "4000");
const archiveDir = process.env.STENCILA_ARCHIVE_DIR || process.env.HOME;
var archive = process.env.STENCILA_ARCHIVE;
if (!archive) {
  for (var name of fs.readdirSync(archiveDir)) {
    if (fs.lstatSync(path.join(archiveDir, name)).isDirectory()) {
      archive = name;
      break;
    }
  }
}
archive = archive || "manuscript";
const baseUrl = process.env.BASE_URL || "/";
const serverUrl = baseUrl + "stencila";
const server = express();

darServer.serve(server, {
  port: port,
  serverUrl: serverUrl,
  rootDir: archiveDir,
  apiUrl: "/archives"
});

// check for local node_modules
let node_modules = path.join(__dirname, "node_modules");
if (!fs.existsSync(node_modules)) {
  node_modules = path.dirname(path.resolve(__dirname));
}
let stencilaDist = path.join(node_modules, "stencila", "dist");

console.log("Stencila app root: %s", stencilaDist);
console.log("DAR archive path: %s", archiveDir);
console.log("DAR public URL: %s", serverUrl);
console.log("Serving stencila on :%s", port);

server.use(logging("dev"));
console.log(stencilaDist);
server.use("/stencilaDist", express.static(stencilaDist));
server.get("/app.js", (req, res) => {
  const appJs = path.join(__dirname, "app.js");
  fs.readFile(appJs, (err, content) => {
    res.append("Content-Type", "application/javascript");
    res.send(
      mustache.render(content.toString(), {
        archive: archive
      })
    );
    res.end();
  });
});
server.use("/", express.static(__dirname));
server.listen(port);
