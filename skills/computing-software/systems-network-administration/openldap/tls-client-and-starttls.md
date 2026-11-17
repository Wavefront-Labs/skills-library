---
id: computing-software.systems-network-administration.openldap.tls-client-and-starttls
name: tls-client-and-starttls
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, starttls, tls-reqcert, tls-cacert, ldaps, ldap-conf, client-tls]
level: practitioner
status: docs-checked
description: "Make OpenLDAP command-line clients use TLS: -Z and -ZZ StartTLS, ldaps URIs, and ldap.conf TLS_CACERT, TLS_CERT, TLS_KEY and TLS_REQCERT."
sources:
  - https://www.openldap.org/doc/admin26/tls.html
  - https://www.openldap.org/software/man.cgi?query=ldap.conf&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS client and StartTLS
Command-line tools:
- `-Z` issues StartTLS and continues without TLS if it fails; `-ZZ` aborts if TLS cannot start.
- `ldaps://host` via `-H` or the `URI` option for LDAP-over-SSL.

Example: `ldapsearch -x -H ldap://ldap.example.com -ZZ -b dc=example,dc=com '(uid=babs)'`

ldap.conf options (system file `/usr/local/etc/openldap/ldap.conf`; user `~/.ldaprc`):
- `TLS_CACERT <file>` = TLSCACertificateFile; `TLS_CACERTDIR <dir>` needs `rehash`.
- `TLS_CERT` / `TLS_KEY` (user-only): client certificate and unencrypted key.
- `TLS_REQCERT {never|allow|try|demand|hard}`: server certificate checks, default `demand`; the guide sees no good reason to change it.
- `TLS_REQSAN` (default `allow`), `TLS_CIPHER_SUITE`, `TLS_PROTOCOL_MIN` (e.g. `3.2` for TLS 1.1; ignored by GnuTLS), `TLS_CRLCHECK none|peer|all` (needs CACERTDIR), `TLS_ECNAME`, `TLS_RANDFILE`.

Example `ldap.conf`:
```
URI ldap://ldap.example.com
BASE dc=example,dc=com
TLS_CACERT /path/to/ca.pem
TLS_REQCERT demand
```
Gotchas: clients often need more trusted CAs than the server; a client certificate DN can be mapped with `authz-regexp` and used with SASL EXTERNAL.

Verify: `ldapwhoami -x -H ldap://host -ZZ`.

## Checked

2026-11-04. Confirmed against the OpenLDAP 2.6 Administrator's Guide chapter 16 (Using TLS) and the ldap.conf(5) page: -Z and -ZZ behaviour, ldaps:// via -H and URI, TLS_CACERT, TLS_CACERTDIR with rehash, user-only TLS_CERT and TLS_KEY, TLS_REQCERT levels and demand default, TLS_REQSAN allow default, TLS_PROTOCOL_MIN 3.2 meaning TLS 1.1, TLS_CRLCHECK levels needing TLS_CACERTDIR, TLS_ECNAME, TLS_RANDFILE, authentication DN mapping for client certificates. Example commands were not run.

Method: documentation only; no commands were run.
