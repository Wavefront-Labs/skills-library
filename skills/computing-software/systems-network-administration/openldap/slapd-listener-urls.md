---
id: computing-software.systems-network-administration.openldap.slapd-listener-urls
name: slapd-listener-urls
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, listener-urls, ldapi, ldaps, pldap, interfaces]
level: practitioner
status: docs-checked
description: "Choose OpenLDAP slapd listener URLs with -h: ldap, ldaps, ldapi, pldap and pldaps, binding to specific interfaces, ports and unix sockets."
sources:
  - https://www.openldap.org/doc/admin26/runningslapd.html
  - https://www.openldap.org/doc/admin26/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slapd listener URLs
Pass one or more space-separated URLs to `slapd -h`. Default is `ldap:///`.

| URL | Meaning |
|---|---|
| `ldap:///` | LDAP, TCP 389 |
| `ldaps:///` | LDAP over SSL, TCP 636 |
| `ldapi:///` | LDAP over a unix-domain socket |
| `pldap:///` | LDAP behind a PROXY protocol v2 proxy (HAProxy), TCP 389 |
| `pldaps:///` | proxied LDAP over SSL, TCP 636 |

Examples:
```
slapd -h "ldaps:// ldap://127.0.0.1:666"
```
This opens ldaps on all interfaces (port 636) and ldap on loopback port 666.

A unix socket path is URL-encoded: `ldapi://%2Fusr%2Flocal%2Fvar%2Fldapi` means `/usr/local/var/ldapi`.

Gotchas:
- By default slapd listens on all IPv4 and IPv6 addresses. `slapd -h ldap://127.0.0.1` disallows remote access.
- Restrict pldap/pldaps at the network level to trusted proxies.
- ldapi is not widely implemented by non-OpenLDAP clients; it pairs with SASL EXTERNAL.

## Checked

2026-11-04. Confirmed against the Administrator's Guide Running slapd and Security chapters: -h default ldap:///, URL table with ports, pldap and pldaps requiring the proxy protocol header and network restriction, the ldaps and loopback port 666 example, hostnames and IPv4/IPv6 addresses, URL-encoded ldapi socket path, ldapi not widely implemented, default listening on IPv4 and IPv6 any addresses, 127.0.0.1 disallowing remote access, SASL EXTERNAL over ldapi. Removed the verify command and the firewall remark.

Method: documentation only; no commands were run.
