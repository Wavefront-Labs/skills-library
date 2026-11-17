---
id: computing-software.networking-hardware-and-wireless.squid.ssl-bump-ca-and-certgen
name: ssl-bump-ca-and-certgen
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, ssl-bump, ca-certificate, sslcrtd-program, security-file-certgen, openssl]
level: sme
status: docs-checked
description: "Create a signing CA and configure the certificate generator (sslcrtd_program) for SSL-Bump."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Intercept/SslBumpExplicit
  - https://www.squid-cache.org/Doc/config/sslcrtd_program/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSL-Bump CA and certificate generator
Build Squid with `--with-openssl --enable-ssl-crtd`. Create a self-signed CA and a DER copy for browsers:
```
openssl req -new -newkey rsa:2048 -sha256 -days 365 -nodes -x509 -extensions v3_ca -keyout myCA.pem  -out myCA.pem
openssl x509 -in myCA.pem -outform DER -out myCA.der
```
Squid side:
```
http_port 3128 ssl-bump \
  cert=/path/to/myCA.pem \
  generate-host-certificates=on dynamic_cert_mem_cache_size=4MB
```
`sslcrtd_program` default: `security_file_certgen -s <ssl_db dir> -M 4MB`. `-s` sets the disk cache directory and `-M` its memory size; without them certificates are created anew per request. Initialise the db, then give Squid access.

Caveats from the page: HTTPS interception raises legal and ethical issues; clients must trust the CA; a leaked CA key enables MITM attacks; avoid `sslproxy_cert_error allow all` and `DONT_VERIFY_PEER`.

## Checked

2026-11-04. Read the SslBumpExplicit wiki page and the sslcrtd_program directive page and confirmed the build options, openssl commands, http_port ssl-bump line, certgen default and the -s and -M behaviour, and the legal and security warnings. Nothing was removed.

Method: documentation only; no commands were run.
