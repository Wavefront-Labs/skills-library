---
id: computing-software.devops-ci-cd.verdaccio.https-with-certificates
name: https-with-certificates
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [https, ssl-certificate, pfx, ssl, tls-certificate, openssl]
level: practitioner
status: docs-checked
description: "Serve Verdaccio over HTTPS by setting listen to an https URL and adding an https block with key, cert and ca, or a pfx file and passphrase."
sources:
  - https://verdaccio.org/docs/ssl/
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/setup-npm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set the protocol in `listen`, then provide certificates.

```yaml
listen: 'https://your.domain.com/'
https:
  key: /path/to/verdaccio-key.pem
  cert: /path/to/verdaccio-cert.pem
  ca: /path/to/verdaccio-csr.pem
```
Self-signed test certificate:
```
openssl genrsa -out verdaccio-key.pem 2048
openssl req -new -sha256 -key verdaccio-key.pem -out verdaccio-csr.pem
openssl x509 -req -in verdaccio-csr.pem -signkey verdaccio-key.pem -out verdaccio-cert.pem
```
A PFX bundle works too (passphrase only if encrypted):
```yaml
https:
  pfx: /path/to/server.pfx
  passphrase: 'secret'
```
Option meanings follow the Node.js TLS docs. Run `verdaccio` and open `https://your.domain.com:port/`.

Docker: set `VERDACCIO_PROTOCOL=https`, because the image CMD provides `listen` and overrides your config entry; set `VERDACCIO_PORT` for a non-4873 port.

Alternative: terminate TLS in a reverse proxy (best practices recommend HTTPS either way). A self-signed cert makes npm fail with `SELF_SIGNED_CERT_IN_CHAIN` unless `strict-ssl` is relaxed.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Set up the SSL Certificates, Configuration (HTTPS) and Setup npm. Confirmed: listen with an https URL, the https block with key, cert and ca, the openssl commands, the pfx and passphrase form, the Docker VERDACCIO_PROTOCOL note and SELF_SIGNED_CERT_IN_CHAIN with strict-ssl. Removed or corrected: nothing.

Method: documentation only; no commands were run.
