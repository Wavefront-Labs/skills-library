---
id: computing-software.systems-network-administration.openldap.network-security-hardening
name: network-security-hardening
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, hardening, ssf, require-authc, disallow, security, bind-anon]
level: practitioner
status: docs-checked
description: "Harden an OpenLDAP server: listener scope, firewalling, SSF requirements, require authc, disallow bind_anon and bind_simple, allow bind_anon_cred and password storage."
sources:
  - https://www.openldap.org/doc/admin26/security.html
  - https://www.openldap.org/software/man.cgi?query=slapd-config&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# network security hardening
Network:
- slapd listens on all addresses by default; `slapd -h ldap://127.0.0.1` blocks remote access but is no substitute for an IP firewall (389/tcp ldap, 636/tcp ldaps).
- TCP Wrappers (`slapd: ALL : DENY` plus allows) act only after the connection is accepted; prefer a firewall.

slapd.conf directives (cn=config: `olcRequires`, `olcDisallows`, `olcAllows`, `olcSecurity`):
```
security ssf=1 update_ssf=112
security simple_bind=56
require authc
disallow bind_anon
disallow bind_simple
allow bind_anon_cred
```
- SSF: 0 none, 1 integrity only, above 1 roughly the key length. `ssf=1 update_ssf=112` requires integrity everywhere and 3DES-equivalent for updates; `simple_bind=56` forces encryption before simple password binds.
- `require authc` demands authentication for directory access; disabling anonymous binds alone does not do that.
- `bind_anon` is enabled by default; `bind_anon_cred` (unauthenticated binds with a DN and empty password) is disabled by default and should stay that way.

Authentication: simple binds send passwords in clear unless TLS or IPsec protects them; SASL and TLS (StartTLS or ldaps) are the standard answers.

Passwords: schemes SSHA (the guide calls it the most secure scheme slapd supports), CRYPT, MD5, SMD5, SHA, SASL pass-through (`{SASL}user@realm`, needs `--enable-spasswd`). Hashes still fall to dictionary attacks.

Verify: an anonymous `ldapsearch -x` against the directory should now be refused once `require authc` is set.

## Checked

2026-11-04. Confirmed against the OpenLDAP 2.6 Administrator's Guide Security Considerations chapter and slapd-config(5): default listen on all addresses and slapd -h, firewall preferred over TCP Wrappers, ports 389 and 636, SSF values and the ssf=1 update_ssf=112 and simple_bind=56 examples, require authc versus disallow bind_anon, bind_anon_cred default disabled, simple bind in clear text, password storage schemes (SSHA, CRYPT, MD5, SMD5, SHA, {SASL}), --enable-spasswd, olcAllows, olcDisallows, olcRequires and olcSecurity attributes. Removed the exact "Strong(er) authentication required" error text, not on those pages, and softened SSHA from preferred to the guide's wording.

Method: documentation only; no commands were run.
