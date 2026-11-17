---
id: computing-software.systems-network-administration.dns-dhcp.kea-ha-tls-between-partners
name: kea-ha-tls-between-partners
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, kea-ha-tls, high-availability, mutual-tls, control-agent]
level: practitioner
status: verified
description: "Secure Kea HA lease updates and heartbeats with TLS and mutual authentication using the dedicated HA listener or the control agent, plus certificate rotation."
sources:
  - https://kea.readthedocs.io/en/latest/arm/security.html
  - https://kea.readthedocs.io/en/latest/arm/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS between HA partners

Kea HA partners send lease updates and heartbeats over HTTP. On untrusted networks (between data
centres, branches) this leaks client data and allows forged updates. TLS for Kea HTTP was added in Kea 1.9.6 and the HA hook
supports HTTPS since 1.9.7 (ARM).

## Dedicated listener with TLS (recommended; the server side is supported since Kea 2.1.7)
```json
"high-availability": [{
  "this-server-name": "kea1",
  "mode": "load-balancing",
  "multi-threading": { "enable-multi-threading": true, "http-dedicated-listener": true, "http-listener-threads": 4, "http-client-threads": 4 },
  "trust-anchor": "/etc/kea/tls/ca.pem",
  "cert-file": "/etc/kea/tls/kea1.pem",
  "key-file": "/etc/kea/tls/kea1.key",
  "require-client-certs": true,
  "peers": [
    { "name": "kea1", "url": "https://10.0.0.11:8001/", "role": "primary" },
    { "name": "kea2", "url": "https://10.0.0.12:8001/", "role": "secondary" }
  ]
}]
```
URLs switch to `https://`, and the host part must be an IPv4 address or an IPv6 address in square
brackets, never a name. Per-peer `trust-anchor`/`cert-file`/`key-file` override the global ones;
the three must be all set or all unset (an empty string counts as unset, which disables HTTPS for
that peer). The HA hook is an HTTPS client, so it has no `cert-required`; the server-side
equivalent is `require-client-certs` (default true, an HA-level not peer-level parameter), and the
peer entry named by `this-server-name` supplies the server's TLS settings.

## Via control agent
Older setups send HA traffic through the Control Agent; configure TLS in `kea-ctrl-agent.conf`
(`trust-anchor`, `cert-file`, `key-file`, `cert-required`) and use https URLs. The Control Agent
was removed in Kea 3.1.8 (development), so use the dedicated listener or an HTTPS control socket on
current releases. For HTTP/HTTPS control sockets, Kea refuses to switch between HTTP and HTTPS on the same
address and port via `config-set` or `config-reload`; change the address or port as well (ARM,
TLS section).

## Certificates
- Use a private CA and PEM files; the ARM notes some libraries enforce a minimum key strength
  (for example RSA 2048). Whether Kea checks the peer's name or IP against the certificate is not
  documented in the ARM, so test it rather than assuming.
- `require-client-certs: true` = mutual TLS; only partners with certs signed by the trust anchor
  can push updates.
- TLS authentication and HTTP basic auth are not bound together (ARM): a valid password does not
  prove the TLS peer is the same party.

## Basic auth
Additionally (or without TLS on trusted networks) `basic-auth-user` (or `basic-auth-user-file`) and
`basic-auth-password` (or `basic-auth-password-file`) per peer. Basic authentication on the HA
dedicated listener was silently ignored before Kea 3.3.1 (changelog entry 2542), so check your
version.

## Verify
- [ ] `ha-heartbeat` succeeds over https, a packet capture on 8001 shows TLS only, and a peer without a valid client cert is rejected.
