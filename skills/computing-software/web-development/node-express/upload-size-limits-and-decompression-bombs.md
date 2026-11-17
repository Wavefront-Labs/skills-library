---
id: computing-software.web-development.node-express.upload-size-limits-and-decompression-bombs
name: upload-size-limits-and-decompression-bombs
category: computing-software
field: web-development
product: node-express
tags: [file-upload-security, secure-file-upload, upload-size-limits, zip-bomb, decompression-bomb, multer-limits, image-bomb, request-body-limit]
level: practitioner
status: verified
description: "Enforcing upload limits at every layer (proxy, body parser, multer, storage) and defending against zip, gzip and pixel-flood decompression bombs."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
  - https://github.com/expressjs/multer#limits
  - https://sharp.pixelplumbing.com/api-constructor
  - https://nginx.org/en/docs/http/ngx_http_core_module.html#client_max_body_size
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upload size limits and decompression bombs

**Goal:** a single request can't exhaust disk, memory or CPU - neither by sheer size nor by a tiny file that expands enormously.

## 1. Limit at every layer
| Layer | Setting |
|---|---|
| Reverse proxy | nginx `client_max_body_size 20m;` (413 early, before the app reads; checked on nginx 1.28 with a 1m limit: a 500 KB POST reached the app, a 3 MB POST got the nginx 413 page and never reached the upstream) |
| Body parsers | `express.json({ limit: '100kb' })`, `express.urlencoded({ limit: '100kb' })` |
| Multipart | multer `limits: { fileSize: 10*1024*1024, files: 5, fields: 20, fieldSize: 100*1024, parts: 30 }` |
| Storage | Presigned POST `content-length-range` |
| Per user | Quotas and rate limits on upload endpoints |
Use multer's disk/stream storage (or stream to S3), not `memoryStorage`, for anything large - memory storage buffers the whole file in RAM per request.

Handle the error cleanly: multer raises `MulterError` with `code === 'LIMIT_FILE_SIZE'` - return 413 with a message.

## 2. Decompression bombs
- **Archives**: a 42 KB zip can expand to petabytes. While extracting, count bytes written and entries; abort above limits (e.g. 500 MB total, 10 000 entries, ratio > 100:1). Never trust the sizes in the zip headers.
- **HTTP request bodies** with `Content-Encoding: gzip`: body parsers inflate them - the `limit` applies to the **inflated** size in body-parser, keep it small (checked: a 51 KB gzip body that inflates to 50 MB was rejected with 413 `entity.too.large` by `express.json({ limit: '100kb' })`).
- **Images (pixel floods)**: a 5 KB PNG can declare 50 000 x 50 000 pixels -> GBs when decoded. sharp has `limitInputPixels` (default 268 megapixels: a generated 20000 x 20000 image was refused with `Input image exceeds pixel limit`; a 26 KB PNG of 3000 x 3000 was accepted by default and refused in about 1 ms at `limitInputPixels: 1000000`; `0` disables the check) - set lower (e.g. 40 MP); Pillow: `Image.MAX_IMAGE_PIXELS`; ImageMagick `policy.xml` resource limits.
- **XML/SVG**: billion-laughs entity expansion - disable DTDs/entities.

## 3. Time limits
Process uploads in background jobs with timeouts; set server `requestTimeout`/`headersTimeout` to stop slow uploads tying up sockets.

## Verify
- [ ] 25 MB upload gets 413 from nginx without app CPU spike.
- [ ] Known zip bomb (e.g. 42.zip) aborts extraction early with a clear error.
- [ ] 50 000x50 000 PNG rejected by the image pipeline in milliseconds.

## Checked
Run on Windows with Node 20.20.2, Express 4.22.3, multer 2.4.0 (and 1.4.5-lts.2 for the behaviour list), file-type 21.3, sharp 0.35, content-disposition 2.0.1 plus nginx 1.28.0 as a reverse proxy: the three checks quoted inline (gzip body through `express.json`, sharp pixel limits, nginx 413). Not run: zip extraction limits (no archive library used), 42.zip, Pillow and ImageMagick limits, presigned POST `content-length-range`, `requestTimeout` and `headersTimeout`, memory use of `memoryStorage`, Linux.
