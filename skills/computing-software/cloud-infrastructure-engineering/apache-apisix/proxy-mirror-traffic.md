---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.proxy-mirror-traffic
name: proxy-mirror-traffic
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, proxy-mirror, traffic-mirroring, sample-ratio, shadow-traffic, plugin]
level: practitioner
status: docs-checked
description: "Mirror a share of APISIX traffic to another host with proxy-mirror: host, path, path_concat_mode, sample_ratio and the plugin_attr timeout settings."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/proxy-mirror.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proxy-mirror traffic

Attributes:
- `host` (required): scheme and address, no path, for example `http://127.0.0.1:8081`.
- `path`: defaults to the route's URI path; ignored for gRPC.
- `path_concat_mode`: `replace` (default) uses `path` as is; `prefix` appends the route's request path. Ignored for gRPC.
- `sample_ratio`: 1 by default, range 0.00001 to 1.

Mirror half of the traffic:

```json
{
  "id": "traffic-mirror-route",
  "uri": "/get",
  "plugins": { "proxy-mirror": { "host": "http://127.0.0.1:8081", "sample_ratio": 0.5 } },
  "upstream": { "nodes": { "httpbin.org": 1 }, "type": "roundrobin" }
}
```

Notes:
- Mirror responses are discarded and never reach clients.
- Mirroring runs as sub-requests, so a slow mirror backend can delay original requests.
- Connect, read and send timeouts default to 60 seconds each; override under `plugin_attr.proxy-mirror.timeout` in `config.yaml` and reload.

## Checked

2026-11-04. Confirmed against the APISIX proxy-mirror plugin page: host, path and path_concat_mode semantics, sample_ratio range, ignored mirror responses, sub-request delay note, 60 second timeout defaults and the plugin_attr override with reload. Nothing removed.

Method: documentation only; no commands were run.
