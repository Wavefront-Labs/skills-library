---
id: computing-software.cloud-infrastructure-engineering.zot.network-conditions-cel
name: network-conditions-cel
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, cel-conditions, client-ip, x-forwarded-for, ip-allowlist, proxy-trust]
level: advanced
status: docs-checked
description: "Restrict Zot policies by client network with CEL conditions on req.client.ip and forwardedFor, avoiding spoofable X-Forwarded-For mistakes behind a proxy."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Conditions go under `accessControl.repositories.<pattern>.policies[].conditions[].expression`.

Variables:
- `req.client.ip`: the TCP peer address. Use for direct connections.
- `req.client.forwardedFor`: `X-Forwarded-For` values. Untrusted, because clients can spoof them.

Never grant access based only on `forwardedFor`. This is insecure:

```cel
req.client.forwardedFor.exists(ip, ip.startsWith("10."))
```

Direct connection:

```cel
req.client.ip.startsWith("10.")
```

Behind a proxy, first confirm the peer is the trusted proxy, then check the forwarded chain:

```cel
req.client.ip == "10.0.0.5" &&
req.client.forwardedFor.size() > 0 &&
req.client.forwardedFor[0].startsWith("192.0.2.")
```

Requirements: the proxy must overwrite `X-Forwarded-For`, and direct access to Zot must be blocked at the network layer, otherwise the trusted-proxy check can be bypassed by clients reaching Zot directly.

## Checked

Network conditions section of the authn-authz page read in full; examples match.

Method: docs-checked 2026-11-09 against zot docs articles/authn-authz.md (network conditions and trusted proxies section).
