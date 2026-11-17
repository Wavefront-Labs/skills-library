---
id: computing-software.networking-hardware-and-wireless.powerdns.pkcs11-softhsm-keys
name: pkcs11-softhsm-keys
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pkcs11, hsm, softhsm, p11-kit, pdnsutil, dnssec]
level: advanced
status: docs-checked
description: "Store PowerDNS DNSSEC keys on a PKCS#11 token: build flag, pkcs11=yes, SoftHSM token init, pdnsutil hsm assign and create-key."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/pkcs11.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKCS#11 keys with SoftHSM

Experimental. Build with `--enable-experimental-pkcs11` (autoconf) or `-Dexperimental-pkcs11=enabled` (Meson); p11-kit libraries and headers are required. Runtime setting `pkcs11=yes` (since 5.2.0).

Local SoftHSM example:
```
apt-get install softhsm p11-kit
p11-kit -l
softhsm2-util --init-token --label my-pkcs11-dnskey --free --pin 1234 --so-pin 1234
pdnsutil hsm assign example.com ecdsa256 ksk softhsm2 my-pkcs11-dnskey 1234 'my key' 'my pub key'
pdnsutil hsm create-key example.com 25
pdnsutil zone show example.com
```
`p11-kit -l` should list `softhsm2`. The `25` is the key ID printed by `assign`.

Notes:
- Assigning a key to a zone requires the token PIN. Afterwards you can remove the PIN or set it empty in the PKCS#11 cryptokey record and log on to the token after starting the server.
- SoftHSM is not recommended for production.
- A physical CryptAS (Athena IDProtect) token is slow, about 1.5 signatures per second as observed, so use it as a hidden primary.
- Builds with `--enable-botan1.10 --enable-experimental-pkcs11` will most likely crash on exit with SoftHSM; Botan support was removed in 4.2.0.

## Checked

2026-11-08. Read in full: PowerDNS docs dnssec/pkcs11.rst. Confirmed the experimental note, both build flags, p11-kit requirement, pkcs11 setting since 5.2.0, the SoftHSM command sequence and its comment about key ID, the PIN note, the not-for-production advice, the Botan crash and 4.2.0 removal, and the CryptAS speed. Reworded the PIN, CryptAS and Botan lines to match the page.

Method: documentation only; no commands were run.
