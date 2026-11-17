---
id: computing-software.web-development.node-express.express-compression-etag-and-static-caching
name: express-compression-etag-and-static-caching
category: computing-software
field: web-development
product: node-express
tags: [express-compression, etag, static-caching, express-static, node-performance]
level: practitioner
status: verified
description: "Compression, ETags and static caching in Express: the compression middleware and SSE pitfalls, express.static maxAge and immutable, ETags, and proxy offload."
sources:
  - https://expressjs.com/en/advanced/best-practice-performance.html
  - https://github.com/expressjs/compression
  - https://expressjs.com/en/api.html#express.static
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# compression, ETag and static caching in Express

## 1. Compression
```js
import compression from "compression";
app.use(compression({
  threshold: 1024,                                       // skip tiny responses
  filter: (req, res) => req.headers["x-no-compression"] ? false : compression.filter(req, res),
}));
```
- compression 1.8.0+ supports Brotli (`br`) when the client accepts it; gzip otherwise; other encodings such as `zstd` are not negotiated (the response goes out uncompressed).
- Prefer compressing at the reverse proxy or CDN (nginx `gzip`/`brotli`, Cloudflare): less CPU in Node, cached compressed variants. Use the middleware when Node is exposed directly or the platform doesn't compress.
- Don't compress already-compressed types (images, video, zip) - the default filter checks `Content-Type` against compressible types.
- **Streaming/SSE**: compression buffers output; call `res.flush()` after each write (the middleware adds it) or exclude `text/event-stream` routes.
- Compressing secrets alongside attacker-controlled input over TLS can enable BREACH; Wikipedia lists CSRF protection and disabling compression (for example for cross-site requests) among the workarounds.

## 2. Static files
```js
app.use("/assets", express.static("dist/assets", {
  maxAge: "1y", immutable: true,                // hashed filenames only
  index: false, fallthrough: true,
}));
app.use(express.static("public", { maxAge: "1h", etag: true, lastModified: true }));
```
- `immutable` + long `maxAge` only for content-hashed files; HTML and unhashed files get short max-age or `no-cache` with validation.
- `setHeaders(res, path)` for per-type headers (e.g. `Content-Disposition` for downloads).
- `dotfiles: "ignore"` (default) keeps `.env`-like files from being served if they end up in the directory.

## 3. ETags
- Express sets weak ETags on `res.send` bodies by default (`app.set("etag", "weak")`); the browser revalidates with `If-None-Match` and gets `304` without the body.
- ETags save bandwidth, not server work: the handler still runs to build the body. For expensive pages, add server-side caching or `Cache-Control` max-age.
- Behind multiple instances, ETags must be consistent across servers (content-based ETags are; inode-based ones from some servers aren't).
- `app.set("etag", false)` for APIs that implement their own versioned ETags.

## 4. Check
```bash
curl -sI -H 'Accept-Encoding: br, gzip' https://example.com/app.js | grep -iE 'content-encoding|cache-control|etag|vary'
```
Expect `Content-Encoding: br`, `Vary: Accept-Encoding`, and `Cache-Control: public, max-age=31536000, immutable` for hashed assets.

## Verify
- [ ] Text responses compressed exactly once (Node or proxy, not both); hashed assets immutable; HTML revalidates; SSE routes stream without buffering.
