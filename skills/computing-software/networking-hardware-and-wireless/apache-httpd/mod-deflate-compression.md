---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-deflate-compression
name: mod-deflate-compression
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-deflate, gzip, compression, setoutputfilter, vary, breach]
level: practitioner
status: docs-checked
description: "Compress responses with mod_deflate: SetOutputFilter vs AddOutputFilterByType, no-gzip exclusions, tuning directives, request decompression, Vary and BREACH."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_deflate.html
  - https://httpd.apache.org/docs/2.4/env.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_deflate compression
Provides the `DEFLATE` output filter; only gzip is supported.

```apache
SetOutputFilter DEFLATE
SetEnvIfNoCase Request_URI "\.(?:gif|jpe?g|png)$" no-gzip
AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
```
`no-gzip` excludes requests; `force-gzip` ignores `Accept-Encoding`.

## Decompression
- `SetOutputFilter INFLATE` inflates gzip backend responses.
- `SetInputFilter DEFLATE` decompresses request bodies sent with `Content-Encoding: gzip`; cap with `DeflateInflateLimitRequestBody`. Content-Length is the compressed size.

## Tuning
| Directive | Default |
|---|---|
| `DeflateCompressionLevel` | zlib default (1-9) |
| `DeflateBufferSize` | 8096 |
| `DeflateMemLevel` | 9 |
| `DeflateWindowSize` | 15 |
| `DeflateFilterNote` | Ratio |

`DeflateFilterNote Input instream` plus a `LogFormat` using `%{instream}n` logs ratios.

## Caches
`Vary: Accept-Encoding` is sent automatically. Add `Header append Vary User-Agent` if compression depends on it; `Header set Vary *` if on other factors.

## Security
Compressing responses mixing secrets with attacker-controlled input over TLS can enable BREACH-style disclosure.

## Checked
2026-11-04. Confirmed against the mod_deflate reference: gzip-only, example configuration, no-gzip/force-gzip, INFLATE and DEFLATE input filters, Content-Length note, directive defaults, DeflateFilterNote logging, Vary handling, BREACH warning. Nothing removed.
Method: documentation only; no commands were run.
