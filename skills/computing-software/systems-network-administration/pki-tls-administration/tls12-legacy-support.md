---
id: computing-software.systems-network-administration.pki-tls-administration.tls12-legacy-support
name: tls12-legacy-support
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [tls12-legacy-support, pki-tls-versions, tls12, tls-legacy, disable-tls10, downgrade, pki-tls-administration]
level: practitioner
status: draft
description: "Keep TLS 1.2 safe, retire TLS 1.0 and 1.1, and size the legacy-client impact before turning protocols off."
sources:
  - https://csrc.nist.gov/pubs/sp/800/52/r2/final
  - https://wiki.mozilla.org/Security/Server_Side_TLS
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TLS 1.2 and legacy client support
Goal: remove obsolete protocol versions without breaking real clients.
- Disable SSLv3, TLS 1.0, TLS 1.1 (RFC 8996). Keep 1.2 until you have measured that no required clients lack 1.3.
- TLS 1.2 requirements: ECDHE key exchange, AEAD (GCM or ChaCha20), no RSA key exchange, no static DH, SHA-2 signatures, `ssl_prefer_server_ciphers off` is fine with a good list.
- Measure first: log `$ssl_protocol` and `$ssl_cipher` in nginx access logs, `log_format ... "$ssl_protocol $ssl_cipher"`; review a week of data.
- Known legacy: Java 7, Android 4.x, Windows XP/IE8, old embedded scanners and payment terminals. Segregate them on a legacy listener if you must serve them.
- Never re-enable TLS 1.0 on the main listener for one client; use a separate hostname or proxy.
Gotcha: disabling TLS 1.2 RSA ciphers breaks nothing modern, but disabling all CBC suites breaks Android 4 and Java 7; check logs before.
Verify:
- [ ] Logs show less than your agreed percentage of legacy protocol use.
- [ ] `nmap --script ssl-enum-ciphers -p 443 host` lists only TLS 1.2 and 1.3.
