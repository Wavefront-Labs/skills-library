---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.remote-auth-ldap-radius
name: remote-auth-ldap-radius
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, ldap-auth, radius-auth, remote-roles]
level: practitioner
status: draft
description: "Configure remote authentication and role mapping on BIG-IP with LDAP or RADIUS plus a local fallback."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote authentication: LDAP, RADIUS, TACACS+

```
tmsh create auth ldap system-auth servers add { 10.1.1.10 } bind-dn "cn=svc-f5,ou=svc,dc=example,dc=com" bind-pw 'xxx' search-base-dn "dc=example,dc=com" ssl enabled ssl-ca-cert-file /Common/corp-ca.crt login-attribute samaccountname
tmsh modify auth remote-user default-role guest remote-console-access disabled
tmsh create auth remote-role role-info add { f5-admins { attribute "memberOf=CN=f5-admins,OU=Groups,DC=example,DC=com" console tmsh line-order 1 role admin user-partition All } }
tmsh create auth radius-server rad1 server 10.1.1.20 secret 'xxx'
tmsh create auth radius system-auth servers add { rad1 }
tmsh modify auth source type ldap
```
- `auth source type` selects `local`, `ldap`, `radius`, `tacacs` or `active-directory`. Accounts not in the remote source still log in only if the `local` method is a fallback; keep `tmsh modify auth source fallback true` and a tested local admin before switching.
- `remote-user default-role` applies when no `remote-role` matches. Set it to `no-access` for least privilege.
- Remote users appear in `tmsh list auth user` after first login with the mapped role (or via the GUI).
- LDAPS: import the CA first (`tmsh install sys crypto cert`).
- Gotcha: management traffic for LDAP leaves via the management route; if the directory is only on a data VLAN, auth fails.

Verify: `tmsh list auth remote-role`, then SSH as a directory user; failures log to `/var/log/secure` and `/var/log/audit` with the bind error.
