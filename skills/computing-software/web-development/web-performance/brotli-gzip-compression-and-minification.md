---
id: computing-software.web-development.web-performance.brotli-gzip-compression-and-minification
name: brotli-gzip-compression-and-minification
category: computing-software
field: web-development
product: web-performance
tags: [javascript-performance, brotli, compression, gzip, minification, zstd]
level: practitioner
status: verified
description: "Shipping smaller text assets: minifying JS/CSS/HTML, Brotli and gzip levels, precompressing static files, zstd, server/CDN configuration, and verifying Content-Encoding."
sources:
  - https://web.dev/articles/reduce-network-payloads-using-text-compression
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding
  - https://nginx.org/en/docs/http/ngx_http_gzip_static_module.html
  - https://github.com/google/ngx_brotli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brotli / gzip compression and minification

## 1. Minify first
Bundlers minify in production builds: esbuild/terser for JS, Lightning CSS/cssnano for CSS, html-minifier-terser for HTML. Check `vite build`/`next build` output is actually minified (mode=production). Minification savings vary with how many comments and long names the source has (measured 87% on lodash.js, which is comment-heavy); the gain after compression is much smaller.

## 2. Compress text responses
| Encoding | Typical savings vs raw JS | Notes |
|---|---|---|
| gzip (level 6) | ~65-80% off raw JS (measured 65% on minified lodash, 82% on unminified) | universal |
| Brotli (11 static / 4-5 dynamic) | 11-33% smaller than gzip -9 at level 11 (measured on lodash, svgo and express files); levels 4-5 are only about as small as gzip -9 | all browsers over HTTPS (Chrome 50, Firefox 44, Safari 11) |
| zstd | similar to Brotli, faster to compress | Chromium 123+, Firefox 126+, Safari 26.3+ (older Safari cannot decode it) - keep Brotli/gzip fallbacks |
Compress: HTML, CSS, JS, JSON, SVG, XML, fonts other than WOFF2 (WOFF2 is already compressed), source maps. Don't recompress images/video/WOFF2/zip.

## 3. Precompress static assets at build
```js
// precompress.mjs - Node's built-in zlib, no extra binaries (run: node precompress.mjs dist)
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import zlib from "node:zlib";
const walk = d => readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(join(d, e.name)) : [join(d, e.name)]);
for (const f of walk(process.argv[2]).filter(f => /\.(js|css|html|svg|json)$/.test(f))) {
  const b = readFileSync(f);
  writeFileSync(f + ".br", zlib.brotliCompressSync(b, { params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 11 } }));
  writeFileSync(f + ".gz", zlib.gzipSync(b, { level: 9 }));
}
```
or the `brotli` CLI (`brotli -q 11 -k file`), or `vite-plugin-compression`. nginx: `brotli_static on; gzip_static on;` serves `.br`/`.gz` siblings. Dynamic responses: Brotli level 4-5 (11 is too slow per request).

## 4. Server/CDN
- Most CDNs (Cloudflare, Fastly, CloudFront with "Compress objects automatically", Vercel, Netlify) compress automatically - ensure origin doesn't double-compress and `Vary: Accept-Encoding` is set.
- Express: `compression()` middleware (gzip/Brotli since v1.8.0; run: serves `br` when `Accept-Encoding: br` is sent, sets `Vary: Accept-Encoding`, skips responses under its 1 KB threshold) - or better, let the reverse proxy/CDN do it.
- Don't compress tiny responses (< ~1 KB).
- Security: compressing responses that mix secrets with attacker-reflected input over TLS enables BREACH - keep CSRF tokens masked or out of compressed reflected pages.

## 5. Beyond compression
Ship less: code splitting, removing unused dependencies, modern-only builds; compression dictionaries (`Use-As-Dictionary`, shared Brotli/zstd dictionaries; `dcb`/`dcz` encodings, Chromium 130+, not shipped in Safari, Firefox behind a preference) can shrink repeat downloads of updated bundles dramatically.

## Verify
`curl -sI -H "Accept-Encoding: br,gzip" https://site/app.js | grep -i content-encoding` -> `br`; DevTools Network shows transferred size much smaller than resource size; Lighthouse "Enable text compression" passes.
