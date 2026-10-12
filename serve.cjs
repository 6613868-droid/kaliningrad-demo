const http = require("http");
const fs = require("fs");
const path = require("path");
const dir = __dirname;
const MIME = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".svg": "image/svg+xml" };
http.createServer((req, res) => {
  let name = decodeURIComponent(req.url.slice(1).split("?")[0]);
  if (!name || name.endsWith("/")) name = "index.html";
  let f = path.join(dir, name);
  fs.readFile(f, (e, d) => {
    if (e) { res.writeHead(404); res.end("no"); return; }
    const type = MIME[path.extname(f).toLowerCase()] || "application/octet-stream";
    res.writeHead(200, { "Content-Type": type, "Cache-Control": "no-store" });
    res.end(d);
  });
}).listen(4178, () => console.log("kaliningrad demo on 4178"));
