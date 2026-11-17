---
id: computing-software.systems-network-administration.dns-dhcp.dnssec-hsm-pkcs11-and-offline-ksk
name: dnssec-hsm-pkcs11-and-offline-ksk
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dnssec, pkcs11, offline-ksk, hsm, key-management]
level: practitioner
status: docs-checked
description: "Protect DNSSEC keys with HSMs via PKCS#11 (OpenSSL provider) in BIND, and run an offline KSK with pre-signed DNSKEY sets."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://github.com/isc-projects/bind9/blob/main/doc/arm/pkcs11.inc.rst
  - https://www.rfc-editor.org/rfc/rfc7512
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSMs/PKCS#11 and offline KSKs

## Why
A stolen KSK lets an attacker sign anything for the zone until the DS changes. High-value zones
keep keys in HSMs or keep the KSK offline.

## BIND with PKCS#11
The ARM says BIND accesses PKCS#11 libraries through OpenSSL providers; for OpenSSL 3 and newer the provider is `pkcs11-provider` (version 0.3 or later required). Configure the provider in an OpenSSL config file (the ARM uses a copy referenced by `OPENSSL_CONF`; `pkcs11-module-load-behavior = early` is required because BIND uses the digest-and-sign API).
```
# create keys in the HSM with pkcs11-tool (OpenSC), as in the ARM example
pkcs11-tool --module <HSM_MODULE> -l -k --key-type rsa:2048 --label example.net-ksk --pin <PIN>
# link the HSM key to BIND key files using a PKCS#11 URI (RFC 7512)
dnssec-keyfromlabel -a RSASHA256 -l "pkcs11:token=bind9;object=example.net-ksk" -f KSK example.net
```
With `dnssec-policy`, a `key-store` block can create keys in the token: `key-store "hsm" { pkcs11-uri "pkcs11:token=bind9"; };` and `keys { ksk key-store "hsm" lifetime unlimited algorithm 13; };` (requires BIND built with OpenSSL 3 and a configured provider; the built-in store `key-directory` is the default).

## Offline KSK model
- ZSK online (signs records continuously), KSK offline (only signs the DNSKEY RRset).
- With `offline-ksk yes;` in the dnssec-policy, BIND does not sign the DNSKEY, CDS and CDNSKEY RRsets; it takes them from Signed Key Response (SKR) files and replaces any such RRsets in the unsigned zone. It is a configuration error to combine `offline-ksk` with a CSK.
- `dnssec-ksr` supports the workflow: `keygen` pregenerates keys for a policy and interval, `request` writes a Key Signing Request with a bundle per period (the published ZSKs), and `sign` signs it to produce the SKR (documented in the 9.20 branch as well as main).
- The KSR/SKR exchange is done periodically, with the KSK kept on an offline host.

## Risks
- Running out of signed key bundles means the signed DNSKEY RRsets expire and validation fails; schedule signing with margin.
- HSM failures stop signing; plan HSM redundancy and key backup per your HSM vendor's documentation.

## Verify
- [ ] `dnssec-verify` passes, the SKR covers the next planned periods, and private KSK material is absent from online hosts.

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus bind-9.20 branch checks), read on 2026-10-26. Confirmed in pkcs11.inc.rst, reference.rst (key-store, pkcs11-uri, offline-ksk) and the dnssec-ksr man page (present on bind-9.20): OpenSSL provider based PKCS#11, pkcs11-provider 0.3+, early load behaviour, pkcs11-tool and dnssec-keyfromlabel example forms with PKCS#11 URIs, key-store requiring OpenSSL 3, offline-ksk behaviour and CSK restriction, ksr keygen/request/sign. Removed unconfirmed engine_pkcs11, native-build, SoftHSM path, quarterly ceremony and root-zone claims.

Method: documentation only; no commands were run.
