---
id: computing-software.software-engineering.deno.http-server-tls-compression-websockets
name: http-server-tls-compression-websockets
category: computing-software
field: software-engineering
product: deno
tags: [http-server, https, tls, websocket, compression, deno-serve, abort-signal]
level: advanced
status: docs-checked
description: "Production Deno.serve features: HTTPS cert/key, HTTP/2, automatic gzip/brotli compression rules, WebSocket upgrade, default fetch export and request abort signal."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/http_server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HTTPS: `cert` and `key` are the PEM contents, not paths.

```ts
Deno.serve({
  port: 8443,
  cert: Deno.readTextFileSync("./cert.pem"),
  key: Deno.readTextFileSync("./key.pem"),
}, (_req) => new Response("Hello over HTTPS!"));
```

Run with `--allow-net --allow-read=cert.pem,key.pem`. HTTP/2 is automatic (also cleartext with prior knowledge).

Compression is off by default: `automaticCompression: true` or `DENO_SERVE_AUTOMATIC_COMPRESSION=1`. gzip and brotli. A body is compressed when `Accept-Encoding` allows `br` or `gzip`, the `Content-Type` is compressible and the body exceeds 64 bytes. Not compressed if the response has `Content-Encoding`, `Content-Range`, or `Cache-Control: no-transform`.

WebSockets (HTTP/1.1 only; the connection cannot carry HTTP afterwards):

```ts
Deno.serve((req) => {
  if (req.headers.get("upgrade") != "websocket") {
    return new Response(null, { status: 426 });
  }
  const { socket, response } = Deno.upgradeWebSocket(req);
  socket.addEventListener("message", (e) => {
    if (e.data === "ping") socket.send("pong");
  });
  return response;
});
```

Default export, run with `deno serve server.ts`:

```ts
export default {
  fetch(request) { return new Response("hi"); },
} satisfies Deno.ServeDefaultExport;
```

`Deno.serve` fires `abort` on a request `signal` even after a successful handler; `--unstable-no-legacy-abort` aborts only on real client disconnect.

## Checked

2026-11-04. Confirmed against the Deno Writing an HTTP Server page: HTTPS cert and key as PEM contents, permissions, HTTP/2, compression off by default with its enabling options and conditions (br or gzip, compressible type, over 64 bytes, exclusions), WebSocket example and HTTP/1.1 limit, default fetch export, abort signal behaviour. Nothing removed.

Method: documentation only; no commands were run.
