---
id: computing-software.systems-network-administration.openldap.access-control-who-selectors
name: access-control-who-selectors
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, who-selectors, peername, dnattr, group-acl, ssf, access-control]
level: practitioner
status: docs-checked
description: "Pick the right by-who selector in OpenLDAP ACLs: anonymous, users, self, dn styles, dnattr, group, peername ip masks, sockurl, and ssf strength factors."
sources:
  - https://www.openldap.org/doc/admin26/access-control.html
  - https://www.openldap.org/software/man.cgi?query=slapd.access&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=slapacl&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# access control who selectors
- `*` everyone; `anonymous` unauthenticated; `users` authenticated; `self` the entry's own DN.
- `dn[.style]=<pattern>` where style is exact, regex, base, one, subtree or children (the same choices as the `to` clause). With a `dn.regex` what clause, the `expand` modifier substitutes the captures: `by dn.exact,expand="uid=$2,dc=example,dc=com" write`.
- `dnattr=<attr>`: requestor DN listed in a DN-valued attribute of the target (e.g. `dnattr=member selfwrite`; also grant `entry`).
- `group[/<objectclass>[/<attr>]][.exact|expand]=<dn>`: defaults `groupOfNames` and `member`. Dynamic groups need a `labeledURI` subtype.
- `peername`, `sockname`, `sockurl`: connection properties. Peername styles: exact (`IP=<ip>:<port>`), `peername.ip=192.168.1.0%255.255.255.0`, `peername.ip=192.168.1.16%255.255.255.240{9009}`, `peername.ipv6=::1`, path.
- `ssf=<n>`, `transport_ssf`, `tls_ssf`, `sasl_ssf`: minimum security strength; 256 is recommended for modern ciphers.
- `domain`: reverse-DNS based and spoofable; avoid.
- `dynacl/aci` (experimental, compile-time) reads the `OpenLDAPaci` attribute by default.
- `real` prefix variants test the authentication DN instead of the authorization DN.

Example: `access to dn.subtree="dc=example,dc=com" by peername.ip=10.0.0.0%255.0.0.0 read by * none`.

Check each rule with `slapacl -b <dn> -D <binddn>`.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide chapter 8 (entity specifiers, dnattr, domain spoofing warning, ssf values and the 256 recommendation) and slapd.access(5) (group defaults groupOfNames and member, dynamic groups need a labeledURI subtype, peername styles and the ip/mask examples, real prefix, dynacl/aci experimental and compile-time with OpenLDAPaci default) and slapacl(8) (-b DN, -D authcDN). Reworded the dn style and aci lines to match the pages.

Method: documentation only; no commands were run.

