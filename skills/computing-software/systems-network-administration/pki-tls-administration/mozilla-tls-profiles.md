---
id: computing-software.systems-network-administration.pki-tls-administration.mozilla-tls-profiles
name: mozilla-tls-profiles
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [mozilla-tls-profiles, pki-cipher-policy, mozilla-ssl-config, tls-profile, intermediate, modern, pki-tls-administration]
level: practitioner
status: draft
description: "Pick a Mozilla server-side TLS profile and generate matching nginx, Apache or HAProxy configuration."
sources:
  - https://wiki.mozilla.org/Security/Server_Side_TLS
  - https://ssl-config.mozilla.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mozilla modern, intermediate and old profiles
Goal: a defensible TLS baseline in minutes.
- Modern: TLS 1.3 only, for clients from about 2019+.
- Intermediate (default recommendation): TLS 1.2 and 1.3, ECDHE with AES-GCM and ChaCha20, RSA 2048+ or ECDSA, HSTS 2 years (confirm values on the page).
- Old: TLS 1.0+ for very old clients; avoid.
Intermediate nginx (shortened; generate current text at ssl-config.mozilla.org):
```
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d; ssl_session_cache shared:MozSSL:10m; ssl_session_tickets off;
```
- Recheck the generator every six months; profiles change.
Gotcha: copying an old blog's cipher list instead of the generator leaves RC4 or CBC suites enabled.
Verify:
- [ ] `testssl.sh --fs host` shows grade A and forward secrecy for all suites.
- [ ] SSL Labs (or Hardenize) result matches the chosen profile.
