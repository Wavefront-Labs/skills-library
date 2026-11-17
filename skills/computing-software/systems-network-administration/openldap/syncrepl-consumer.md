---
id: computing-software.systems-network-administration.openldap.syncrepl-consumer
name: syncrepl-consumer
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, syncrepl, refreshonly, refreshandpersist, replication, olcsyncrepl, consumer]
level: practitioner
status: docs-checked
description: "Configure an OpenLDAP syncrepl consumer: rid, provider, searchbase, type refreshOnly or refreshAndPersist, retry, bindmethod, keepalive, partial replication."
sources:
  - https://www.openldap.org/doc/admin26/replication.html
  - https://www.openldap.org/software/man.cgi?query=slapd.conf&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# syncrepl consumer
The consumer pulls via RFC 4533 and maintains a shadow copy. Configure it on the consumer, with `overlay syncprov` on the provider.

```
syncrepl rid=123
        provider=ldap://provider.example.com:389
        type=refreshOnly
        interval=01:00:00:00
        searchbase="dc=example,dc=com"
        filter="(objectClass=organizationalPerson)"
        scope=sub
        attrs="cn,sn,ou,telephoneNumber,title,l"
        bindmethod=simple
        binddn="cn=syncuser,dc=example,dc=com"
        credentials=secret
updateref ldap://provider.example.com
```
cn=config: `olcSyncRepl` (same parameters, as in the admin guide's cn=config examples).

Parameters:
- `rid`: non-negative integer not greater than 999 (three decimal digits). `searchbase` is required; scope defaults to `sub`, filter to `(objectclass=*)`, attrs to `*,+`.
- `type`: `refreshOnly` (poll; default interval one day, `interval=dd:hh:mm:ss`) or `refreshAndPersist` (provider pushes changes).
- `retry="60 10 300 3"`: interval/count pairs; `+` means retry forever, e.g. `retry="60 +"`.
- `bindmethod`: `simple` (needs TLS or IPsec) or `sasl`. `starttls=yes|critical`; `tls_reqcert` defaults to `demand`.
- `keepalive="240:10:30"`; `suffixmassage` maps remote to local suffix.
- Partial replication: sparse via `filter`, fractional via `attrs`.

Gotcha: the sync identity needs appropriate access (ACLs) to the replicated data and unlimited size and time limits on the provider (or an appropriate `limits` statement), or the replica is incomplete. Leave the consumer `sizelimit` and `timelimit` at their defaults. If no `retry` is given, syncrepl retries every hour forever. Turn `schemachecking` off with partial replication.

## Checked

2026-11-09. Confirmed against the admin guide replication chapter (syncrepl example, sparse and fractional replication, RFC4533) and the slapd.conf(5) syncrepl section (rid limit, defaults, types, retry, bindmethod, keepalive, starttls, tls_reqcert, suffixmassage, identity limits, updateref). Removed: the `olcUpdateref` attribute name, not seen on the fetched pages. The slapdconfig.html source was replaced by the slapd.conf(5) man page.
Method: documentation only; no commands were run.
