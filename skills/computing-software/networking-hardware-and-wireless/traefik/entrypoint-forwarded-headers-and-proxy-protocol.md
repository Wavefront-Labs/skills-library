---
id: computing-software.networking-hardware-and-wireless.traefik.entrypoint-forwarded-headers-and-proxy-protocol
name: entrypoint-forwarded-headers-and-proxy-protocol
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, forwardedheaders, trustedips, proxyprotocol, x-forwarded-for, entrypoints]
level: practitioner
status: docs-checked
description: "Trust X-Forwarded-* headers or PROXY protocol only from known load balancers using forwardedHeaders.trustedIPs and proxyProtocol.trustedIPs."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/entrypoints.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# entrypoint forwarded headers and proxy protocol
Behind a load balancer, Traefik must learn the real client address and scheme. Two entrypoint features do it. `forwardedHeaders` options: `trustedIPs`, `insecure` (trust everyone), `connection`, `addXForwardedSchemeHeaders` and `notAppendXForwardedFor`. `proxyProtocol` options: `trustedIPs` and `insecure`.

```yaml
entryPoints:
  websecure:
    address: ":443"
    forwardedHeaders:
      trustedIPs:
        - "10.0.0.0/8"
    proxyProtocol:
      trustedIPs:
        - "10.0.0.0/8"
```
`trustedIPs` takes the IPs or CIDRs from which Traefik trusts the forwarded headers information (X-Forwarded-*). The `10.0.0.0/8` range above is an example.

Gotchas: `forwardedHeaders.insecure` always trusts the forwarded headers, and the reference recommends it for tests only, not production. `notAppendXForwardedFor: true` stops Traefik appending the client address to X-Forwarded-For and preserves an existing header as is. With PROXY protocol enabled the entrypoint accepts connections with or without PROXY protocol headers, supports versions 1 and 2, and detects the version automatically.

## Checked
2026-11-03. Confirmed against the Traefik entrypoints reference page: the `forwardedHeaders` options (`trustedIPs`, `insecure`, `connection`, `addXForwardedSchemeHeaders`, `notAppendXForwardedFor`) and the `proxyProtocol` options with their descriptions. Removed: the claim that untrusted headers are replaced, the claim that a PROXY protocol mismatch breaks every connection (the page says connections with or without the header are accepted), the version hedge and the forged-header Verify step.
Method: documentation only; no commands were run.


