---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.server-ssl-profile
name: server-ssl-profile
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, serverssl, re-encryption, server-side-tls]
level: practitioner
status: draft
description: "Re-encrypt traffic to pool members with a server SSL profile, validate backend certificates and present client certs."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-ssl-administration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Server SSL profile and re-encryption

```
tmsh create ltm profile server-ssl sssl_app defaults-from serverssl server-name app.internal authenticate once ca-file /Common/corp-ca.crt peer-cert-mode require ciphers "ECDHE+AES-GCM"
tmsh modify ltm virtual vs_web profiles add { sssl_app { context serverside } }
tmsh modify ltm profile server-ssl sssl_app cert-key-chain replace-all-with { client { cert bigip-client.crt key bigip-client.key } }
```
- The built-in `serverssl` profile accepts any backend certificate; it only encrypts. For validation set `peer-cert-mode require` (or `request`), `authenticate once|always` and `ca-file` with the trust chain.
- `server-name` sets the SNI sent to the pool member, required by many hosted backends. `sni-default` and `sni-require` exist for multi-host backends.
- Present a client certificate to backends needing mutual TLS through `cert-key-chain`.
- Offload only: leave out serverssl and send HTTP to the members. Bridging (SSL on both sides) allows iRules/HTTP profile to inspect cleartext in the middle.
- `ssl-forward-proxy` (SSL Orchestrator/forward proxy) is a separate feature and out of scope here.
- Gotcha: cipher mismatches with the backend show as "SSL handshake failed" in `/var/log/ltm`, and members are not marked down by TCP monitors. Use an HTTPS monitor that uses its own ssl-profile.

Verify: `tmsh show ltm profile server-ssl sssl_app`, then `openssl s_client -connect member:443` to confirm what the backend offers; tcpdump on the serverside VLAN shows the handshake after the VS accepts a request.
