---
id: computing-software.systems-network-administration.openldap.monitor-backend
name: monitor-backend
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, monitor, cn-monitor, monitoring, counters, backend-monitor]
level: practitioner
status: docs-checked
description: "Enable and query the OpenLDAP cn=Monitor backend: configuration, restricting access, ldapsearch commands, and the Operations, Connections, Statistics and Threads entries."
sources:
  - https://www.openldap.org/doc/admin26/monitoringslapd.html
  - https://www.openldap.org/software/man.cgi?query=slapd-monitor&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# monitor backend
cn=config:
```
dn: olcDatabase=monitor,cn=config
objectClass: olcDatabaseConfig
olcDatabase: monitor
```
slapd.conf: include `core.schema`, add `database monitor` below the other databases. No `suffix`: the base is always `cn=Monitor`, and only one monitor database is allowed. Built in by default (`--enable-monitor=yes`).

Restrict it, as the data can be sensitive:
```
database monitor
access to * by dn.exact="cn=Manager,dc=example,dc=com" read by * none
```
Queries:
```
ldapsearch -x -D 'cn=Manager,dc=example,dc=com' -W -b 'cn=Monitor' -s base 1.1
ldapsearch -x -D 'cn=Manager,dc=example,dc=com' -W -b 'cn=Monitor' -s base '(objectClass=*)' '*' '+'
ldapsearch -x -D 'cn=Manager,dc=example,dc=com' -W -b 'cn=Monitor' -s sub 1.1
```
Entries: Backends, Connections (`cn=Total`, `cn=Current`), Databases, Listener, Log, Operations (Initiated/Completed by type), Overlays, Statistics (`cn=Entries`, Bytes, PDU, Referrals), Threads (`cn=Max`), Time, Waiters (`cn=Read`, `cn=Write`). SASL and TLS are empty.

`cn=Log` accepts `description` values (Trace, Packets, Args, Conns, BER, Filter, Config, ACL, Stats, Stats2, Shell, Parse, Sync) to change logging live. The backend ignores size and time limits.

## Checked

2026-11-04. Confirmed against the Administrator's Guide Monitoring chapter and slapd-monitor(5): cn=config and slapd.conf setup, core.schema requirement, fixed cn=Monitor suffix and single instance, access restriction example, the three ldapsearch commands, entries Backends, Connections (Total, Current), Databases, Listener, Log with its description values, Operations, Overlays, SASL and TLS empty, Statistics, Threads (Max), Time, Waiters (Read, Write), --enable-monitor=yes default, size and time limits not honoured.

Method: documentation only; no commands were run.
