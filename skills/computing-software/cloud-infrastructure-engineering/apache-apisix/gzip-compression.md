---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.gzip-compression
name: gzip-compression
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, gzip, compression, content-encoding, comp-level, plugin]
level: intro
status: docs-checked
description: "Compress APISIX responses with the gzip plugin: types, min_length, comp_level, http_version, buffers and vary, and the APISIX-Runtime requirement."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/gzip.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gzip compression

Each attribute maps to an NGINX gzip directive:
- `types`: array of MIME types or `"*"`; default `["text/html"]` (`gzip_types`).
- `min_length`: 20 (`gzip_min_length`).
- `comp_level`: 1, range 1-9.
- `http_version`: 1.1 or 1.0 (default 1.1).
- `buffers.number`: 32 and `buffers.size`: 4096 bytes.
- `vary`: false (`gzip_vary`).

```json
{
  "uri": "/index.html",
  "plugins": {
    "gzip": {
      "types": ["text/html", "application/json"],
      "comp_level": 5,
      "buffers": { "number": 8, "size": 4096 }
    }
  },
  "upstream": { "type": "roundrobin", "nodes": { "127.0.0.1:1980": 1 } }
}
```

Notes:
- Requires APISIX-Runtime.
- Clients must send `Accept-Encoding: gzip`; compressed responses carry `Content-Encoding: gzip`.
- To remove the plugin, resubmit the route without the `gzip` block; no restart is needed.

## Checked

2026-11-04. Confirmed against the APISIX gzip plugin page: all attribute defaults and ranges, APISIX-Runtime requirement, Accept-Encoding and Content-Encoding behaviour, removal without restart. Nothing removed.

Method: documentation only; no commands were run.
