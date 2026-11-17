---
id: computing-software.networking-hardware-and-wireless.apache-httpd.ip-host-and-variable-access-control
name: ip-host-and-variable-access-control
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, access-control, require-ip, require-host, require-not, mod-authz-host, migration]
level: practitioner
status: docs-checked
description: "Restrict access by IP, host name or request variables using Require ip, Require host, Require not inside RequireAll, If and Require expr, replacing Order/Allow/Deny."
sources:
  - https://httpd.apache.org/docs/2.4/howto/access.html
  - https://httpd.apache.org/docs/2.4/mod/mod_authz_core.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IP, host and variable access control
## By address (mod_authz_host)
```apache
Require ip 10.2.3.4
Require ip 172.20
Require ip 192.168.1.0/24
Require ip 2001:db8:1::/48
Require host example.org
```
`Require ip` takes a full or partial IP (`172.20` matches 172.20.0.0/16), a network/netmask pair or CIDR; IPv4 or IPv6. `Require host` takes full or partial domain names.

## Negation
`not` cannot stand alone. Pair it with something that can evaluate true:
```apache
<RequireAll>
    Require all granted
    Require not ip 10.252.46.165
</RequireAll>
Require not host phishers.example.com badguys.example
```

## By variable
```apache
<If "%{HTTP_USER_AGENT} == 'BadBot'">
    Require all denied
</If>
Require expr %{HTTP_USER_AGENT} != 'BadBot'
```
User-Agent checks are unreliable because clients set any value.

## mod_rewrite
`[F]` returns 403, but the docs say `<If>` often replaces mod_rewrite here.

## Migration
`Order`, `Allow` and `Deny` live in mod_access_compat and are deprecated; avoid them and outdated tutorials that use them.

## Trap
`<Limit>` inside `<Location>` can silently override `<Directory>` restrictions (see the configuration sections merging documentation).

## Checked
2026-11-04. Confirmed against the Access Control how-to: Require ip and host forms and address formats, not with RequireAll, If and Require expr examples, User-Agent warning, mod_rewrite [F] and If note, mod_access_compat deprecation, Limit inside Location warning. Removed the claim about mixing with Require and the Satisfy mention, which the page does not support.
Method: documentation only; no commands were run.
