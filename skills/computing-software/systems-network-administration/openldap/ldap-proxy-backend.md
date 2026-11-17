---
id: computing-software.systems-network-administration.openldap.ldap-proxy-backend
name: ldap-proxy-backend
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, back-ldap, idassert-bind, acl-bind, proxy, chase-referrals]
level: advanced
status: docs-checked
description: "Configure the OpenLDAP ldap backend as a proxy: uri lists, acl-bind, idassert-bind and idassert-authzFrom, referral chasing, TLS, timeouts, onerr and norefs."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapd-ldap&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP proxy backend
```
database ldap
suffix   "dc=example,dc=com"
uri      ldap://localhost/ ldap://remotehost
```
`uri` takes several servers; the first to answer is used and a responding backup moves to the front. Directives must follow `database ldap`.

- `acl-bind bindmethod=simple|sasl binddn=... credentials=...`: identity for ACL checks and privileged operations. Default is anonymous (empty simple bind). Not used for anonymous clients.
- `idassert-bind bindmethod=none|simple|sasl ... [authz=native|proxyauthz] [mode=legacy|anonymous|none|self]`: asserts authenticated clients' identities. Defaults: `bindmethod=none`, `authz=proxyauthz`, `mode=legacy`. The remote identity needs proxy-authz rights, and the remote server needs `authz-policy` `to` or `both`.
- `idassert-authzFrom <authz-regexp>`: which local identities may use assertion (here `*` allows anonymous).
- `chase-referrals {YES|no}`: default chasing on. `rebind-as-user {NO|yes}`.
- `tls {none|[try-]start|[try-]propagate|ldaps}`: StartTLS unless the URI is ldaps; `tls_reqcert` defaults to `demand`.
- `network-timeout`, `timeout [<op>=]<val>`, `keepalive <idle>:<probes>:<interval>`.
- `norefs yes`: drop search references. `onerr {CONTINUE|stop}`. `noundeffilter yes`: return success on undefined filters.

Gotcha: each explicit bind session gets its own remote connection; anonymous sessions share one.

## Checked

2026-11-09. Confirmed against slapd-ldap(5) in the OpenLDAP 2.6 manual (uri list behaviour, acl-bind, idassert-bind defaults and options, idassert-authzFrom, chase-referrals, rebind-as-user, tls, timeouts, keepalive, norefs, onerr, noundeffilter, connection handling). Dropped the unread Admin Guide backends chapter from sources.

Method: documentation only; no commands were run.

