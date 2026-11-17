---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.mtls-apisix-to-upstream
name: mtls-apisix-to-upstream
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, mtls, upstream-tls, client-cert, tls, apisix-runtime]
level: advanced
status: docs-checked
description: "Present a client certificate from APISIX to an upstream: PATCH tls.client_cert and client_key (or client_cert_id) on the upstream, for HTTP and stream, needing APISIX-Runtime."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/mtls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mTLS from APISIX to an upstream

Requires APISIX-Runtime. Patch the upstream with the client certificate and key:

```shell
curl http://127.0.0.1:9180/apisix/admin/upstreams/1 \
-H "X-API-KEY: $admin_key" -X PATCH -d '
{
    "tls": {
        "client_cert": "<CLIENT_CERT_PEM>",
        "client_key": "<CLIENT_KEY_PEM>"
    }
}'
```

Notes:
- The stream (L4) subsystem supports this too: set `tls.client_cert` and `tls.client_key`, or `tls.client_cert_id`, on an upstream using the `tls` scheme.

## Checked

2026-11-04: read the mTLS page (APISIX to upstream section); tls.client_cert and client_key, the APISIX-Runtime requirement, the PATCH to /apisix/admin/upstreams/1 on 9180 and the stream-subsystem note match. Removed a filler line about the PATCH response body.

Method: documentation only; no commands were run.
