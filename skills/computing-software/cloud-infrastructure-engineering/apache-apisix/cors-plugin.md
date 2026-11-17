---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.cors-plugin
name: cors-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, cors, allow-origins, preflight, allow-credential, plugin]
level: practitioner
status: docs-checked
description: "Configure the APISIX cors plugin: allow_origins, methods, headers, expose_headers, max_age, allow_credential, regex origins, metadata origins and timing origins."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/cors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cors plugin

Attributes and defaults:
- `allow_origins`: `"*"`; comma-separated `scheme://host:port`.
- `allow_methods`: `"*"`; `allow_headers`: `"*"`.
- `expose_headers`: unset leaves `Access-Control-Expose-Headers` unchanged.
- `max_age`: 5 seconds; -1 disables preflight caching.
- `allow_credential`: false.
- `allow_origins_by_regex`: array of regexes; overrides `allow_origins`.
- `allow_origins_by_metadata`: keys that refer to plugin metadata origins.
- `timing_allow_origins` and `timing_allow_origins_by_regex`: origins allowed to read resource timing.

Metadata (`plugin_metadata/cors`) has `allow_origins`, an object mapping keys to origin strings.

```json
"cors": {
  "allow_origins": "http://sub.domain.com,http://sub2.domain.com",
  "allow_methods": "GET,POST",
  "allow_headers": "headr1,headr2",
  "expose_headers": "ex-headr1,ex-headr2",
  "max_age": 50,
  "allow_credential": true
}
```

Notes:
- With `allow_credential` true, the wildcard defaults stop working; list origins, methods and headers explicitly.
- The value `**` forces all values even with credentials, which exposes you to CSRF-type risks.
- Disallowed origins get no CORS headers but still receive the upstream's 200.
- Escape regex dots as `\\.` inside JSON.

## Checked

2026-11-04. Confirmed against the APISIX cors plugin page: attribute defaults, the ** wildcard caveat with credentials, disallowed-origin behaviour, regex escaping in JSON. Nothing removed.

Method: documentation only; no commands were run.

