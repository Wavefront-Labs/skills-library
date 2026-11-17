---
id: computing-software.cloud-infrastructure-engineering.zot.mutual-tls-identity
name: mutual-tls-identity
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, mtls, client-certificates, identity-attributes, uri-san-pattern, spiffe]
level: advanced
status: docs-checked
description: "Enable Zot mutual TLS with a CA cert and choose how identity is extracted from client certificates: attributes, URI SAN regex and SAN indexes."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Setting `cacert` enables mTLS; client certificates are validated against it:

```json
"auth": { "tls": { "cert": "/etc/zot/certs/server.cert", "key": "/etc/zot/certs/server.key", "cacert": "/etc/zot/certs/ca.cert" } }
```

Identity extraction under `auth.mtls`:

```json
"mtls": { "identityAttributes": ["URI", "CommonName"],
  "uriSanPattern": "spiffe://example.org/workload/(.*)",
  "uriSanIndex": 0, "dnsSanIndex": 0, "emailSanIndex": 0 }
```

- `identityAttributes`: case-insensitive, tried in order with fallback. Names: `CommonName`/`CN`, `Subject`/`DN`, `Email`/`rfc822name`, `URI`/`URL`, `DNSName`/`DNS`. Default `["CommonName"]`.
- `uriSanPattern`: regex extracting identity from the URI SAN; if absent the full URI is used. With the pattern above, `spiffe://example.org/workload/testuser` yields `testuser`.
- `uriSanIndex`, `dnsSanIndex`, `emailSanIndex`: 0-based index into multi-valued SAN fields, default 0.

The extracted identity is then matched against `accessControl` policies. mTLS is evaluated after basic auth and session auth in the priority order.

## Checked

2026-11-04. Read against the zot authn-authz article (Mutual TLS section); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
