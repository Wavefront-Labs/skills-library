---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.proxy-rewrite-uri
name: proxy-rewrite-uri
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, proxy-rewrite, uri, regex-uri, rewrite, host, method, plugin]
level: practitioner
status: docs-checked
description: "Rewrite the upstream URI, method or host in APISIX with proxy-rewrite: uri, regex_uri pairs, priority rules, and use_real_request_uri_unsafe."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/proxy-rewrite.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proxy-rewrite URI

Attributes (none required; only `use_real_request_uri_unsafe` has a default):
- `uri`: new upstream path; supports NGINX variables such as `$arg_name`.
- `regex_uri`: flat array of pattern and replacement pairs, tried in order, first match wins.
- `method`: rewrites the HTTP method (GET, POST, PUT, PATCH, DELETE and others).
- `host`: sets the `Host` request header.
- `use_real_request_uri_unsafe`: false; true bypasses URI normalization (unsafe).

If both `uri` and `regex_uri` are set, `uri` takes priority.

Examples:

```json
"proxy-rewrite": { "uri": "/anything" }
```

```json
"proxy-rewrite": { "uri": "/get?arg1=apisix&arg2=plugin" }
```

```json
"proxy-rewrite": { "regex_uri": ["^/test/(.*)/(.*)", "/$1-$2"] }
```

The regex example sends `/test/user/agent` upstream as `/user-agent`. Several pairs go in one array, for example `["^/test/(.*)/(.*)", "/$1-$2", "^/other/(.*)", "/other"]`.

Set the Host header with the `host` attribute, not with `headers.set`. With the `radixtree_uri_with_parameter` router, route parameters are available as `uri_param_*` variables.

## Checked

2026-11-04: read the proxy-rewrite plugin page; attributes (uri, method list, regex_uri pairs with first match and uri precedence, host, use_real_request_uri_unsafe default false), and the /anything, /get?arg1=apisix&arg2=plugin and ^/test/(.*)/(.*) examples match. Nothing removed.

Method: documentation only; no commands were run.
