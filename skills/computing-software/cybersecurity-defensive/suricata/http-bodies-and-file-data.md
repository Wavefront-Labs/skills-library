---
id: computing-software.cybersecurity-defensive.suricata.http-bodies-and-file-data
name: http-bodies-and-file-data
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [http-request-body, http-response-body, file-data, body-limits]
level: advanced
status: docs-checked
description: "Inspect HTTP bodies: http.request_body, http.response_body, file.data, body-limit settings, chunked inspection and negated-match cautions."
sources: ["https://docs.suricata.io/en/latest/rules/http-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bodies and file.data

- `http.request_body`: client body; amount inspected set by `request-body-limit` in the libhtp config.
- `http.response_body`: server body, matching decompressed gzip or deflate data; limited by `response-body-limit`.
- `file.data`: similar, also covers request bodies and non-HTTP protocols.

Large bodies are inspected in chunks. Negated matches can misfire across chunks, so add a `depth`. Decompression of Flash (SWF) files must be enabled in the libhtp configuration.

Defaults in suricata.yaml: libhtp `request-body-limit` 3072 and `response-body-limit` 3072, personality `IDS`. A value of 0 means unlimited.

`http.stat_msg` is always empty for HTTP/2. For HTTP/2, `http.request_header` and `http.response_header` join name and value with a colon and space; use `http2.header_name` for a colon inside a name.

## Checked

2026-11-04. Confirmed against the HTTP Keywords page (request_body, response_body, stat_msg, file.data, chunked inspection and negation, Flash decompression, HTTP/2 header joining) and the suricata.yaml configuration page (libhtp defaults).

Method: documentation only; no commands were run.
