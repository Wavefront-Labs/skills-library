---
id: computing-software.systems-network-administration.openldap.tls-server-configuration
name: tls-server-configuration
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, tls, tlscertificatefile, tlsverifyclient, tlscacertificatefile, tlsciphersuite, ldaps]
level: practitioner
status: docs-checked
description: "Configure TLS on OpenLDAP slapd: certificate, key and CA files, cipher suites, DH parameters, EC curves and TLSVerifyClient modes for SASL EXTERNAL."
sources:
  - https://www.openldap.org/doc/admin26/tls.html
  - https://www.openldap.org/software/man.cgi?query=slapd-config&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS server configuration
Requirements: a valid X.509 server certificate whose CN is the server FQDN (subjectAltName may hold aliases and wildcards).

Global directives (slapd.conf; cn=config uses `olcTLS*` names):
```
TLSCACertificateFile /path/to/ca.pem
TLSCertificateFile   /path/to/server.crt
TLSCertificateKeyFile /path/to/server.key
TLSVerifyClient never
```
- `TLSCACertificateFile`: PEM of trusted CAs, including intermediates up to the root. `TLSCACertificatePath` needs OpenSSL `rehash` and symlinks; the file is recommended.
- `TLSCertificateKeyFile`: must be unencrypted; protect it.
- `TLSCipherSuite`: list OpenSSL ciphers with `openssl ciphers -v ALL` (GnuTLS: `gnutls-cli -l`).
- `TLSDHParamFile`: needed for DHE suites, DSA keys, RSA certificates without key encipherment. `openssl dhparam -out <file> <numbits>`.
- `TLSECName`: EC curve for ECDHE (OpenSSL only); list with `openssl ecparam -list_curves`.
- `TLSRandFile`: only if /dev/urandom is unavailable.
- `TLSVerifyClient {never|allow|try|demand}` default `never`: allow = request, continue on failure; try = continue only if none given; demand = require valid. SASL EXTERNAL requires a non-default value and a valid client certificate.

Enable the listener: `slapd -h "ldap:/// ldaps:///"`.

## Checked

2026-11-04. Confirmed against the Administrator's Guide Using TLS chapter and slapd-config(5): server certificate CN as FQDN with subjectAltName aliases, TLSCACertificateFile and chain advice, TLSCACertificatePath with rehash and symlinks, TLSCertificateKeyFile unencrypted, TLSCipherSuite with openssl ciphers -v ALL and gnutls-cli -l, TLSRandFile, TLSDHParamFile conditions and openssl dhparam, TLSECName with openssl ecparam -list_curves, TLSVerifyClient modes and default never, SASL EXTERNAL needing a non-default setting, olcTLS* names. Removed the ldapsearch verify command, which the pages do not give.

Method: documentation only; no commands were run.
