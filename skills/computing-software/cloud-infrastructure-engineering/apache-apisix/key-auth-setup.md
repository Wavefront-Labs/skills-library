---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.key-auth-setup
name: key-auth-setup
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, key-auth, api-key, authentication, consumer, credential, plugin]
level: intro
status: docs-checked
description: "Protect an APISIX route with key-auth: create a consumer and credential, enable the plugin, choose header or query name, hide credentials, and read the 401 messages."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/key-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# key-auth setup

1. Create the consumer: `{"username":"jack"}` to `/apisix/admin/consumers`.
2. Add a credential with PUT to `/apisix/admin/consumers/jack/credentials`:

```json
{"id":"cred-jack-key-auth","plugins":{"key-auth":{"key":"<API_KEY>"}}}
```

The `key` can be encrypted in etcd, read from `$env://`, or pulled from `$secret://`.

3. Enable the plugin on a route with `"plugins":{"key-auth":{}}`.

Route attributes:
- `header`: default `apikey`.
- `query`: default `apikey`; lower priority than `header`.
- `hide_credentials`: false; true strips the key before the upstream.
- `anonymous_consumer`: consumer name that lets unauthenticated requests through.
- `realm`: `key` by default (APISIX 3.15.0+), used in `WWW-Authenticate`.

Test:
- `curl -i "http://127.0.0.1:9080/anything" -H 'apikey: <API_KEY>'` returns 200.
- Wrong key: 401 `{"message":"Invalid API key in request"}`.
- No key: 401 `{"message":"Missing API key found in request"}`.

## Checked

2026-11-04. Confirmed against the APISIX key-auth plugin page: key attribute, header and query names, env and secret references, both 401 messages. Nothing removed.

Method: documentation only; no commands were run.

