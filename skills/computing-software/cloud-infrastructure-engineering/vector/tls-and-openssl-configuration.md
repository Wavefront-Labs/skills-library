---
id: computing-software.cloud-infrastructure-engineering.vector.tls-and-openssl-configuration
name: tls-and-openssl-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [tls, openssl, certificates, fips, legacy-provider, ca-bundle, vector]
level: sme
status: docs-checked
description: "Control trusted CAs, OpenSSL config and providers for Vector's statically linked OpenSSL."
sources:
  - https://vector.dev/docs/reference/configuration/tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Official Vector binaries are statically linked against OpenSSL and do not use the system library.

**Trusted certificates.** OpenSSL reads `SSL_CERT_FILE` (one file with many certificates) and `SSL_CERT_DIR`. Vector also probes common OS locations using the openssl-probe crate. Disable the probing with `--openssl-no-probe` or `VECTOR_OPENSSL_NO_PROBE`. Set `SSL_CERT_FILE` or `SSL_CERT_DIR` for Vector only to pin specific CAs.

**OpenSSL configuration.** Read from `OPENSSL_CONF` or the default `/usr/local/ssl/openssl.cnf`. Prefer `OPENSSL_CONF` for Vector alone, because other applications may read the default file.

**Providers.** The default provider is used, with modern algorithms. The legacy provider (MD2, RC4 and similar) and the FIPS provider must be loaded through an OpenSSL config:

```ini
openssl_conf = openssl_init
[openssl_init]
providers = provider_sect
[provider_sect]
default = default_sect
legacy = legacy_sect
[default_sect]
activate = 1
[legacy_sect]
activate = 1
```

```bash
OPENSSL_CONF=/path/to/openssl-legacy.cnf vector --config /path/to/vector.yaml
```

The FIPS provider restricts TLS to approved algorithms but does not make Vector fully FIPS compliant; see the linked issue in the docs.

## Checked

Method: docs-checked 2026-11-09 against the full Vector TLS configuration page (raw markdown from the vectordotdev/vector repo). Dropped an unsourced note about the probe and the exec source, and a verification line.
