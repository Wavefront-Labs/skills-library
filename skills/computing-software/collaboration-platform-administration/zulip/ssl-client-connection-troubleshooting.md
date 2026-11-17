---
id: computing-software.collaboration-platform-administration.zulip.ssl-client-connection-troubleshooting
name: ssl-client-connection-troubleshooting
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [tls-troubleshooting, android-tls, ios-tls-version, ssl-ecdh-curve]
level: advanced
status: docs-checked
description: "Diagnose Zulip mobile app TLS failures: incomplete chain on Android, TLS 1.2 on iOS, and Android 7.0 elliptic curve secp256r1 issues with nginx ssl_ecdh_curve."
sources: ["https://zulip.readthedocs.io/en/latest/production/ssl-certificates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mobile app TLS connection problems

Android app cannot connect: most often an incomplete certificate chain. Ensure `/etc/ssl/certs/zulip.combined-chain.crt` contains the full chain with intermediates, and verify with SSL Labs (check "Chain issues") or curl.

iOS app cannot connect: the server may support only TLS 1.1 or older (including TLS 1.0, SSL 3 or SSL 2). Apple has required TLS 1.2 for app connections since iOS 9, and major browsers also require 1.2 or later. Check supported versions with the SSL Labs tester if the server is public. The fix is to support TLS 1.2 and preferably 1.3; in nginx, set the `ssl_protocols` directive.

Android connects on some devices only: Android 7.0 has a bug in its system TLS stack and supports only the elliptic curve `secp256r1` for ECDHE, not `secp384r1` or `secp512r1`. If your server offers only other curves, 7.0 clients fail. nginx, and therefore a default Zulip server, offers `secp256r1` among others; you can control the offered curves with `ssl_ecdh_curve` in the nginx configuration.

Two signs it is this issue rather than something else:

- Only Android 7.0 is affected; 7.1.1 and later are fixed.
- In SSL Labs, under "Cipher Suites", `TLS_ECDHE` lines show `ECDH secp256r1` or `secp384r1`; the problem applies if `secp256r1` is not offered.

Always test with a tool rather than a desktop browser, because browsers ignore errors that apps do not.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/ssl-certificates.html (zulip.readthedocs.io, latest). Removed: the claim that the curve issue appears only if curves were restricted.

Method: documentation only; no commands were run.
