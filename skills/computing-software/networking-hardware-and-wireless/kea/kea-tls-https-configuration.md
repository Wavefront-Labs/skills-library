---
id: computing-software.networking-hardware-and-wireless.kea.kea-tls-https-configuration
name: kea-tls-https-configuration
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, tls, https, trust-anchor, cert-file, key-file, cert-required]
level: advanced
status: docs-checked
description: "Configure Kea TLS with trust-anchor, cert-file, key-file and cert-required: file formats, library differences, and the all-or-none rule."
sources:
  - https://kea.readthedocs.io/en/latest/arm/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea TLS/HTTPS configuration
Parameters:
- `trust-anchor`: file or directory holding the peer's CA certificate. With OpenSSL a directory must include hash symbolic links; with Botan it is searched recursively.
- `cert-file`: this Kea instance's end-entity certificate.
- `key-file`: its private key. It must not be encrypted, so restrict access to it.
- `cert-required`: server-side flag; default true means the client certificate is required and the client must be authenticated. It has no meaning on the client side.

The three string parameters must be all unspecified (TLS disabled) or all specified (TLS enabled). TLS is asymmetric: authenticating the server to the client is mandatory, authenticating the client to the server is optional.

Files must be PEM. Files with several certificates are untested and unsupported. Botan needs standard CA attributes on CA certificates, version 3 end-entity certificates and PKCS 8 private keys. Botan and recent OpenSSL enforce minimal key strength, for example RSA of at least 2048 bits.

The sample certificates in the Kea sources (src/lib/asiolink/testutils/ca) are for testing only, not production. Handshake failures can have many causes and error messages often do not pinpoint them.

## Checked

2026-11-08. Read the Kea Security chapter sections 5.1 to 5.2 in full: the TLS parameters trust-anchor, cert-file, key-file and cert-required, the all-or-none rule, PEM, Botan and OpenSSL differences, key strength, and the test-only sample certificates. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
