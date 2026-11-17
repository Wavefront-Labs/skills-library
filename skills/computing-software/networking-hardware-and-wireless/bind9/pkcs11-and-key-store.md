---
id: computing-software.networking-hardware-and-wireless.bind9.pkcs11-and-key-store
name: pkcs11-and-key-store
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, pkcs11, hsm, key-store]
level: advanced
status: docs-checked
description: "Keep BIND 9 DNSSEC keys in an HSM through OpenSSL 3 pkcs11-provider, key-store pkcs11-uri, and dnssec-keyfromlabel."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter5.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pkcs11 and key store
PKCS#11 support goes through the OpenSSL 3 pkcs11-provider (version 0.3 or later). Its `openssl.cnf` needs `pkcs11-module-load-behavior = early`.

Create keys on the token with `pkcs11-tool`, then reference them:

```
dnssec-keyfromlabel -a RSASHA256 -l "pkcs11:token=bind9;object=example.net-ksk;pin-value=0000" -f KSK example.net
```

For automatic management use a `key-store` with `pkcs11-uri` and name it in `keys { ... key-store name ...; }`. The built-in store is `key-directory`.

## Checked

2026-11-04. Read the PKCS#11 section of the DNSSEC chapter and the key-store block definition: pkcs11-provider 0.3 or later, early load behaviour, pkcs11-tool, the dnssec-keyfromlabel example, key-store pkcs11-uri and the built-in key-directory store confirmed. Nothing was removed.

Method: documentation only; no commands were run.
