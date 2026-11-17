---
id: computing-software.systems-network-administration.varnish-cache.compression-gzip
name: compression-gzip
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [gzip, do-gzip, do-gunzip, http-gzip-support]
level: practitioner
status: docs-checked
description: "Control compression: default Accept-Encoding handling, compress text before storing with beresp.do_gzip, decompress with do_gunzip, and turn gzip support off."
sources:
  - https://www.varnish.org/docs/users-guide/compression/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# compression gzip

Compression defaults to on (Varnish 4.0 onward). To stop Varnish touching the encoding, set the parameter `http_gzip_support` to false.

## Default behaviour

Active when `http_gzip_support` is on and neither `beresp.do_gzip` nor `beresp.do_gunzip` is used in VCL.
- Unless `vcl_recv` returns pipe or pass, `req.http.Accept-Encoding` is set to "gzip" if the client supports gzip, otherwise removed.
- Unless the request is a pass, `bereq.http.Accept-Encoding` is set to "gzip" before `vcl_backend_fetch` runs, so VCL can change it.
- A gzipped backend response is stored compressed in memory and `Accept-Encoding` is added to `Vary`.
- Clients supporting gzip get the compressed content unmodified; others get it decompressed on the fly, with `Content-Encoding` removed and any ETag weakened (`W/` prefix).
- For Vary lookups, Accept-Encoding is ignored.

## Compress when the backend does not

```vcl
sub vcl_backend_response {
    if (beresp.http.content-type ~ "text") {
        set beresp.do_gzip = true;
    }
}
```

Before insertion this sets `obj.http.Content-Encoding` to gzip, adds Accept-Encoding to `obj.http.Vary` unless present, and weakens any ETag. The page argues Varnish uses little CPU, so compressing there may beat CPU-bound web or app servers. Do not compress uncompressable content such as JPG, GIF and MP3; it wastes CPU.

## Decompress before caching

`set beresp.do_gunzip = true;` removes `obj.http.Content-Encoding` and weakens any ETag. A use case is working around a badly configured backend that compresses already-compressed content such as JPG; fixing the backend is better.

## ESI and turning gzip off

ESI and gzip work together: Varnish decompresses to do the ESI processing, then recompresses for storage and delivery.

With `http_gzip_support` off, Varnish makes none of the header changes above, handles `Vary: Accept-Encoding` like any other Vary value, and ignores `beresp.do_gzip` and `beresp.do_gunzip`.

## Checked

Method: 2026-11-08, read the Varnish compression page in full (docs only, nothing run). Restructured to the page's sections; added the pass/pipe and bereq.Accept-Encoding details, the "default applies only when do_gzip and do_gunzip are unused" condition and the page's CPU rationale. Claims were otherwise unchanged.
