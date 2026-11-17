---
id: computing-software.data-engineering.apache-nifi.site-to-site-properties
name: site-to-site-properties
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, site-to-site, s2s, nifi-properties, raw, http]
level: practitioner
status: docs-checked
description: "Server-side Site-to-Site keys: nifi.remote.input.host, secure, socket port for RAW, HTTP enabled, transaction TTL, contents cache and route settings for reverse proxies."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site-to-Site in nifi.properties

- `nifi.remote.input.host`: from the local hostname lookup by default.
- `nifi.remote.input.secure`: true.
- `nifi.remote.input.socket.port`: blank; must be set to use RAW transport.
- `nifi.remote.input.http.enabled`: true.
- `nifi.remote.input.http.transaction.ttl`: 30 secs.
- `nifi.remote.contents.cache.expiration`: 30 secs.
- Routes for reverse proxies: `nifi.remote.route.{protocol}.{name}.when`, `.hostname`, `.port`, `.secure` (secure defaults to false; the others have no default).

Receiving data from a remote NiFi needs a root-level Input Port; serving pulls uses a root-level Output Port.

Verify: a Remote Process Group pointed at this instance lists the ports and transmits without a connection error.

## Checked

Checked against the NiFi Administration Guide Site-to-Site properties and routing sections and the User Guide Remote Process Group section: host default, secure true, RAW port blank, HTTP enabled true, 30 sec transaction TTL and cache expiration, the route property names and `secure` default of false, and Input Ports added to the Root Process Group match.

Method: docs-only read of cited pages, 2026-11-08
