---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.proxy-rewrite-headers
name: proxy-rewrite-headers
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, proxy-rewrite, headers, request-headers, consumer-name, plugin]
level: practitioner
status: docs-checked
description: "Add, set or remove request headers before the upstream with APISIX proxy-rewrite headers: execution order, array values, variables and the Host caveat."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/proxy-rewrite.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proxy-rewrite headers

`headers` holds three actions, executed in the order add, remove, set:
- `add`: appends a value and keeps any client value.
- `set`: overwrites existing values.
- `remove`: array of header names to delete.

Values may be constants, NGINX variables, `regex_uri` captures, or (APISIX 3.18.0+) arrays that produce repeated header lines.

Set example:

```json
"proxy-rewrite": { "headers": { "set": { "X-Api-Version": ["v1", "v2"], "X-Api-Engine": "apisix" } } }
```

Here the client's `X-Api-Version` is replaced. With `add` instead, a client value `client` becomes `["client","v1","v2"]`.

Remove:

```json
"proxy-rewrite": { "headers": { "remove": ["User-Agent"] } }
```

Forward the consumer name and drop the API key:

```json
"headers": { "set": { "X-Apisix-Consumer": "$consumer_name" }, "remove": ["Apikey"] }
```

Route parameters can be passed on with `"X-User-Id": "$uri_param_user_id"` under the `radixtree_uri_with_parameter` router.

Do not set `Host` with `headers.set`; use the `host` attribute.

## Checked

2026-11-04: read the proxy-rewrite plugin page; headers add, remove and set order, array values from APISIX 3.18.0, the set and add client-value examples, the consumer name and Apikey example, the uri_param_user_id example and the Host caveat match. Nothing removed.

Method: documentation only; no commands were run.
