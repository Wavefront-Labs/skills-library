---
id: computing-software.data-engineering.apache-nifi.tls-toolkit
name: tls-toolkit
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, toolkit, tls-toolkit, certificates, keystore, ca]
level: advanced
status: docs-checked
description: "tls-toolkit.sh modes: standalone, server and client with key flags and defaults (RSA 2048, SHA256WITHRSA, 825 days, jks, CA port 9443, DN prefix CN=, suffix OU=NIFI)."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/toolkit-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tls-toolkit

`./bin/tls-toolkit.sh`

standalone:
- `-n` hostnames (ranges like `[01-20]`, counts `(N)`), `-C` client DN, `-O` overwrite, `-o` output dir (default `../bin`)
- `-S`/`-P`/`-K` keystore, truststore, key passwords; `-f` base nifi.properties
- `-a` RSA, `-k` 2048, `-s` SHA256WITHRSA, `-d` 825 days, `-T` jks, `-c` CA host localhost
- `--nifiDnPrefix` `CN=`, `--nifiDnSuffix` `, OU=NIFI`, `--subjectAlternativeNames`, `--additionalCACertificate`

server:
- `-p` port 9443, `-t` token (required), `-D` CA DN default `CN=YOUR_CA_HOSTNAME,OU=NIFI`, `-f` config JSON default `config.json`

client:
- `-c` CA host, `-p` 9443, `-t` token, `-C` cert dir (default `.`), `-D` DN, `-T PKCS12` for browser import

Verify: generated keystores list the expected hostnames and NiFi trusts the CA.

The guide recommends JKS stores for NiFi, says the tool ignores PKCS12 as a truststore type, and does not support wildcard certificates (each node needs its own CN and SAN).

## Checked

Checked against the NiFi Toolkit Guide, TLS Toolkit section: every standalone, server and client flag and default in the skill (RSA, 2048, SHA256WITHRSA, 825 days, jks, port 9443, DN prefix and suffix, config.json, token required, `-T PKCS12` for browser import) matches the option lists. Added the guide's JKS and wildcard notes. Nothing was removed.

Method: docs-only read of cited pages, 2026-11-08
