---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-authentication-and-digest-algorithms
name: pjsip-authentication-and-digest-algorithms
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, auth, digest, sha-256, password-digest, realm, 401]
level: advanced
status: docs-checked
description: "Configure PJSIP auth objects: auth_type digest, realm handling, pre-hashed password_digest, and supported_algorithms_uas/uac for MD5, SHA-256 and SHA-512-256 challenges."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/PJSIP-Authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip authentication and digest algorithms
SHA-256 and SHA-512-256 digests need a recent PJProject (2.15.1 bundled with Asterisk 20.12.0, 21.7.0 and 22.2.0) plus a suitable OpenSSL; MD5 is always supported. Run `pjproject show buildopts` to see supported algorithms.

Flow: as UAS, Asterisk answers 401 with `WWW-Authenticate` headers built from the endpoint's `auth` object (realm, nonce, algorithm). As UAC, it picks an `outbound_auth` object whose realm matches (or is empty or `*`) and builds an `Authorization` header.

Parameters:
- `auth_type`: `digest` or `google_oauth`. `userpass` and `md5` are deprecated and converted to `digest`.
- `password` is plain text; `password_digest = <ALGORITHM>:<hash>` is the pre-hashed form of `<username>:<realm>:<password>`, at most one per algorithm. `md5_cred` is deprecated.
- Hash with `echo -n "user:realm:pass" | openssl dgst -md5`; `-n` matters because line endings would change the hash. Algorithm names are `MD5`, `SHA-256`, `SHA-512-256`.
- `realm`: for UAS it defaults to the global `default_realm`, then `asterisk`. For UAC leave empty or `*` unless you know the UAS realm.
- `supported_algorithms_uas` (order of challenges, falls back to global `default_auth_algorithms_uas`, then `MD5`) and `supported_algorithms_uac`.
- `nonce_lifetime`, `refresh_token`, `oauth_clientid`, `oauth_secret`.

Use separate auth objects for `auth` and `outbound_auth` on one endpoint unless the realms are known.

## Checked

2026-11-09. Confirmed against the Asterisk PJSIP Authentication page: PJProject 2.15.1 and Asterisk 20.12.0, 21.7.0 and 22.2.0, pjproject show buildopts, auth_type values and deprecations, realm defaults, password_digest format, supported_algorithms_uas and uac defaults, separate auth objects. Nothing changed.
Method: documentation only; no commands were run.
