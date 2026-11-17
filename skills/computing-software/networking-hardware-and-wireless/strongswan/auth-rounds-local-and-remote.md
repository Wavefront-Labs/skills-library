---
id: computing-software.networking-hardware-and-wireless.strongswan.auth-rounds-local-and-remote
name: auth-rounds-local-and-remote
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, authentication, local-remote, identities, revocation, signature-constraints]
level: practitioner
status: docs-checked
description: "Configure strongSwan local and remote authentication rounds: auth methods, ids with wildcards and regex, certs and cacerts, ca_id, signature constraints and revocation policy."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# auth rounds local and remote
Each connection has `local` and `remote` sections. Several rounds use suffixes (`local-xauth`, `remote2`) for IKEv2 multiple authentication or IKEv1 XAuth; `round` orders them.

`auth` methods: `pubkey` (default), `psk`, `xauth` (IKEv1; a backend name may follow a dash) and `eap` (a method name may be appended with a dash, e.g. `eap-tls`). For IKEv2 signature authentication use `ike:` constraints, e.g. `ike:pubkey-sha384-sha256`, or `rsa/pss` for RSASSA-PSS.

Remote constraints: key type and minimum strength (`ecdsa-384`, `rsa-2048-ecdsa-256`) and hash lists (`pubkey-sha256-sha512`); for EAP-TLS append a colon, e.g. `eap-tls:ecdsa-384-sha384`.

- `id`: with certificates it must be in the certificate (subject DN or subjectAltName); defaults to the subject DN. On `remote`, default `%any`; wildcards such as `*@strongswan.org` or `"C=CH, O=strongSwan, CN=*"` work, exact matches preferred. Regex needs a type prefix, `^` and `$`, e.g. `email:^(moon|sun)@strongswan\.org$` (page says since 6.0.2).
- `eap_id`, `aaa_id`, `xauth_id`: identities for the EAP or XAuth exchange.
- `certs` (local: candidates chosen via certificate requests; remote: accepted certs), `cacerts`, `pubkeys`, `ca_id`, `cert_policy`, `groups`.
- `revocation`: `relaxed` (default, fails only if revoked), `ifuri` (fails only if a CRL/OCSP URI exists but checking fails), `strict` (fails if no revocation information is available).

## Checked
2026-11-04. Confirmed against the local and remote sections of the swanctl.conf page: auth keywords and constraints, id wildcards and regex rules, certs, cacerts, pubkeys, ca_id, cert_policy, groups and revocation defaults.

Method: documentation only; no commands were run.
