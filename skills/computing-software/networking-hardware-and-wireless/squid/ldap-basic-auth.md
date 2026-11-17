---
id: computing-software.networking-hardware-and-wireless.squid.ldap-basic-auth
name: ldap-basic-auth
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, ldap, squid-ldap-auth, basic-auth, bind-dn]
level: practitioner
status: docs-checked
description: "Authenticate Basic credentials against LDAP with the squid_ldap_auth helper and its bind, base and filter options."
sources:
  - https://wiki.squid-cache.org/ConfigExamples/Authenticate/Ldap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP authentication
```
auth_param basic program /usr/lib/squid/squid_ldap_auth -v 3 -b "dc=yourcompany,dc=com" -D uid=some-user,ou=People,dc=yourcompany,dc=com  -w password -f uid=%s ldap.yourcompany.com
auth_param basic children 5
auth_param basic realm Web-Proxy
auth_param basic credentialsttl 1 minute
acl ldap-auth proxy_auth REQUIRED
http_access allow ldap-auth
```
Helper options: `-b` base DN, `-D` and `-w` bind DN and password (omit both for anonymous bind), `-f` search filter with `%s` as username, `-ZZ` TLS to the LDAP server, last argument the LDAP host. For Windows 2003 AD use the filter `sAMAccountName=%s`.

Caveats: the helper line must not wrap; TLS protects only Squid-to-LDAP traffic, not browser-to-Squid.

## Checked

2026-11-04. Read the Authenticate/Ldap wiki page and confirmed the helper line, anonymous bind, -ZZ, the Windows 2003 filter and the no-wrap and TLS scope notes. Removed the claim that the bind password sits in plaintext, which the page does not state.

Method: documentation only; no commands were run.
