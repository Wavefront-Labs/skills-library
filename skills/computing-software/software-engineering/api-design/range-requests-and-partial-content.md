---
id: computing-software.software-engineering.api-design.range-requests-and-partial-content
name: range-requests-and-partial-content
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, range-requests, http-206, content-range, accept-ranges, resumable-download, if-range, rfc-9110]
level: practitioner
status: docs-checked
description: "Serve large downloads with HTTP range requests: Accept-Ranges, 206 and 416 responses, Content-Range, If-Range validators and resumable client logic."
sources: ["https://www.rfc-editor.org/rfc/rfc9110#section-14", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Range requests and partial content (RFC 9110 section 14)

Lets clients fetch part of a representation: resume interrupted downloads, stream media, read a file tail. Range requests are an optional HTTP feature; a server that does not support them answers as for a normal GET.

## Exchange
```http
GET /exports/big.csv HTTP/1.1
Range: bytes=1000000-1999999
If-Range: "v7"

HTTP/1.1 206 Partial Content
Accept-Ranges: bytes
Content-Range: bytes 1000000-1999999/5242880
Content-Length: 1000000
ETag: "v7"
```
- Advertise support with `Accept-Ranges: bytes`; a server with no range support for the resource may send `Accept-Ranges: none`. Clients may send Range without it, and must not assume a later request will get a partial response.
- Range applies to GET only; a server MUST ignore Range on other methods and on range units it does not understand, and MAY ignore Range altogether.
- If the range is valid but unsatisfiable (or the unit is unsupported), the server SHOULD send `416 Range Not Satisfiable`, with `Content-Range: bytes */5242880` giving the current length.
- Byte offsets start at zero and are inclusive. `bytes=500-` (open-ended) and `bytes=-500` (the last 500 bytes) are valid; a last position at or past the end means the remainder.
- `If-Range` makes the range conditional on an ETag or a Last-Modified date (not both); if the condition fails the server sends the whole resource with 200, so a client never splices two versions. Range is evaluated after the other preconditions and is ignored when a conditional GET would give 304.
- Several comma-separated ranges return a 206 with `multipart/byteranges`, each part carrying its own `Content-Type` and `Content-Range`. A server may ignore or reject a request with more than two overlapping ranges or many small out-of-order ranges (denial-of-service risk); clients should list ranges in ascending order and avoid multiple ranges that cost more than one covering range.
- `Content-Range` complete length may be `*` when unknown, for example `bytes 42-1233/*`.

## Client resume
Check support with a HEAD request and look for `Accept-Ranges` with a value other than `none`. To resume, send `Range: bytes=<bytes already stored>-` plus `If-Range` with the stored ETag or date, and append only when the answer is 206 with a matching `Content-Range`.

## Gotchas
- Range support on dynamically generated bodies needs stable bytes; a changing body breaks resume.
- With a content coding applied, byte ranges refer to the encoded bytes, not the decoded ones; avoid compressing ranged binary files.
- Check that every intermediary you deploy (cache, proxy, CDN) passes range requests through correctly.

Verify: `curl -i -H "Range: bytes=0-9" <url>` returns `206` with `Content-Range: bytes 0-9/<total>` and 10 bytes; a first position past the end returns `416`.

## Checked
2026-11-08. Confirmed against RFC 9110 section 14 (read in full: range units, byte ranges, Range, Accept-Ranges, Content-Range, multipart/byteranges) and the MDN Range requests guide (If-Range, support check, statuses). Removed: curl `-C`/`-r` resume examples, "only byte ranges are registered" and the CDN-behaviour claim (not in the sources). RFC 9110 section 13.1.5 (If-Range rules) was not read; the If-Range behaviour is from the MDN guide.
Method: documentation only; no commands were run.
