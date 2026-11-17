---
id: computing-software.networking-hardware-and-wireless.strongswan.pkcs12-bundles-for-clients
name: pkcs12-bundles-for-clients
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, pkcs12, openssl, client-certificates, android]
level: practitioner
status: docs-checked
description: "Build PKCS#12 containers with openssl for Windows, Android, macOS and iOS strongSwan clients, including the legacy option, Android CA warning and DER to PEM conversion."
sources:
  - https://docs.strongswan.org/docs/latest/pki/pkiQuickstart.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pkcs12 bundles for clients
Windows, Android, macOS and iOS clients usually need key, certificate and CA certificate in one PKCS#12 file. The pki tool cannot create these; use openssl:

```
openssl pkcs12 -export -inkey carolKey.pem \
               -in carolCert.pem -name "carol" \
               -certfile strongswanCert.pem -caname "strongSwan Root CA" \
               -out carolCert.p12
```

- Apple and Android clients only process containers protected with 3DES and the legacy KDF. With OpenSSL 3.0 or newer the `-legacy` option is required.
- On Android 4.4 and later a CA certificate inside the container triggers the warning "Network may be monitored by an unknown third party". Omit `-certfile`, import the PKCS#12 into the trust store, and import the CA certificate directly into the strongSwan app (or install both via a configuration profile).
- Use several `-certfile` arguments for multi-level chains.
- openssl needs PEM input. Generate with `--outform pem` or convert: `openssl x509 -inform der -outform pem -in cert.der -out cert.pem`, and `openssl ec` or `openssl rsa` with `-inform der -outform pem` for keys.

## Checked
2026-11-04. Confirmed against the strongSwan PKI Quickstart page: openssl pkcs12 command, 3DES and legacy KDF for Apple and Android with the -legacy option on OpenSSL 3.0 and newer, Android 4.4 warning workaround, multiple -certfile, DER to PEM conversions. Nothing removed.

Method: documentation only; no commands were run.
