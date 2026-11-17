---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.redirect-plugin
name: redirect-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, redirect, http-to-https, ret-code, regex-uri, plugin]
level: practitioner
status: docs-checked
description: "Redirect requests in APISIX with the redirect plugin: http_to_https, uri, regex_uri, ret_code, encode_uri, append_query_string and X-Forwarded-Proto trust."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/redirect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# redirect plugin

Attributes:
- `http_to_https`: false; true redirects HTTP to HTTPS with the same URI (301).
- `uri`: target URI; supports NGINX variables.
- `regex_uri`: a `[pattern, replacement]` pair; non-matching requests go to the upstream.
- `ret_code`: 302 by default (200 or higher).
- `encode_uri`: false; encodes `Location` per RFC 3986.
- `append_query_string`: false; appends the original query string.

Use only one of `http_to_https`, `uri` or `regex_uri`. `http_to_https` cannot be combined with `append_query_string`.

```json
{
  "uri": "/old",
  "plugins": { "redirect": { "uri": "/new", "ret_code": 301 } }
}
```

Scheme detection uses `X-Forwarded-Proto` if present, otherwise the connection scheme. An inbound `X-Forwarded-Proto` is kept only from addresses in `apisix.trusted_addresses`; otherwise APISIX overwrites it.

HTTPS port priority: `plugin_attr.redirect.https_port`, then a random port from `apisix.ssl.listen`, then 443.

## Checked

2026-11-04. Confirmed against the APISIX redirect plugin page: attributes, scheme detection through X-Forwarded-Proto and trusted_addresses, HTTPS port priority. Nothing removed.

Method: documentation only; no commands were run.

