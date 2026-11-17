---
id: computing-software.cryptography-implementation.protocol-implementation.private-trust-anchors-and-custom-trust-stores
name: private-trust-anchors-and-custom-trust-stores
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, certificate-validation, custom-trust-store, private-root, trust-anchor, ca-bundle, update-ca-certificates, java-truststore, requests-ca-bundle, node-extra-ca-certs]
level: practitioner
status: docs-checked
description: "Trust a private CA without disabling verification: Debian update-ca-certificates, Python requests, Node NODE_EXTRA_CA_CERTS and Java keytool settings."
sources: ["https://manpages.debian.org/stable/ca-certificates/update-ca-certificates.8.en.html", "https://requests.readthedocs.io/en/latest/user/advanced/", "https://nodejs.org/api/cli.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/keytool.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private trust anchors and custom trust stores

Internal services signed by a private CA fail validation by default. Do not turn verification off: Python requests warns that `verify=False` accepts any certificate, ignores hostname mismatches and expiry, and leaves the application open to man-in-the-middle attacks. Add the private root as a trust anchor instead, as narrowly as possible.

## Debian and Ubuntu system store
`update-ca-certificates` manages the machine's CA collection (individual files in `/etc/ssl/certs`, plus the concatenated `ca-certificates.crt`).
- Copy each certificate in PEM format with a `.crt` extension into `/usr/local/share/ca-certificates`, one certificate per file, then run `update-ca-certificates`. Certificates with a `.crt` extension there are implicitly trusted.
- Distribution CAs are listed in `/etc/ca-certificates.conf`; a line starting with `!` deselects a CA.

## Runtimes with their own settings
| Runtime | Documented setting |
|---|---|
| Python requests | `verify` accepts a path to a CA bundle file or a directory processed with OpenSSL `c_rehash`, or set `REQUESTS_CA_BUNDLE` (falls back to `CURL_CA_BUNDLE`). Requests uses certificates from the `certifi` package by default and the docs recommend upgrading certifi often. The prepared-request flow ignores environment variables, so merge environment settings into the session. |
| Node.js | `NODE_EXTRA_CA_CERTS=file` extends the well-known root CAs with PEM certificates from the file; it is read only at process start. `--use-system-ca` (added in v23.8.0; non-Windows/macOS support in v23.9.0) uses the system store. |
| Java | `keytool -importcert` imports a certificate into a keystore; `-cacerts` accesses the JDK's `cacerts` keystore and `-trustcacerts` trusts certificates from cacerts when building chains. Supply the keystore password with `-storepass`. |

## Verify
- [ ] No code disables verification.
- [ ] Each runtime connects to the internal service with verification on.

## Checked
Method: docs-checked 2026-11-09 against the Debian update-ca-certificates(8) page, the Requests "Advanced Usage" page (SSL cert verification, CA certificates), the Node.js CLI documentation (NODE_EXTRA_CA_CERTS, --use-system-ca) and the JDK 21 keytool man page (importcert options; the full page was searched by option rather than read end to end).
Removed as unconfirmed by the cited pages: RHEL, macOS and Windows commands, Go, curl and .NET rows, the keytool default password, container image advice, name-constraining the private CA, and root rotation guidance.
