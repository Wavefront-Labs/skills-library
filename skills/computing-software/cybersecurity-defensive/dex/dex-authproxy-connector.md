---
id: computing-software.cybersecurity-defensive.dex.dex-authproxy-connector
name: dex-authproxy-connector
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [authproxy, connector, headers, reverse-proxy]
level: advanced
status: docs-checked
description: "Delegate login to a front-end proxy with the Dex authproxy connector: X-Remote-User and X-Remote-Group headers and header stripping."
sources:
  - https://dexidp.io/docs/connectors/authproxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The experimental authproxy connector returns identities from authentication done by a front-end web server. Dex reads the `X-Remote-User` header as the user's email and `X-Remote-Group` as the group.

```yaml
connectors:
- type: authproxy
  id: myBasicAuth
  name: HTTP Basic Auth
  config:
    userHeader: X-Forwarded-User
    groupHeader: X-Forwarded-Group
    staticGroups:
    - default
```

- `userHeader` default `X-Remote-User`; `groupHeader` default `X-Remote-Group`.
- `staticGroups` are added to any groups from the header.

The proxy must authenticate the user only on the callback path `(dex issuer URL)/callback/(connector id)?(query)`, for example `https://auth.example.com/dex/callback/slack?state=...`. After login it returns the user to that exact URL, query included, with the header set to the user's email.

Security: the proxy MUST remove any `X-Remote-*` headers sent by the client, on any URL path, before forwarding to Dex. The Apache example does this with `RequestHeader unset X-Remote-User` on `/dex/` and sets it from `REMOTE_USER` on the callback location.

Gotchas: the connector does not support refresh tokens, and the Apache example is marked as requiring Apache 2.4.10+.

## Checked

2026-11-03: read against Dex docs, authproxy connector (https://dexidp.io/docs/connectors/authproxy/).

Removed or corrected: Reworded the Apache version remark.

Method: documentation only; no commands were run.
