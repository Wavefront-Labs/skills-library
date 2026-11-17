---
id: computing-software.systems-network-administration.samba.net-ads-commands
name: net-ads-commands
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, net-ads-commands, net-ads, ads-keytab, net, active-directory]
level: practitioner
status: docs-checked
description: "Use net ads for AD membership tasks: join, leave, testjoin, status, DNS register, changetrustpw, search, SPNs, enctypes, keytab create and kerberos kinit."
sources:
  - https://www.samba.org/samba/docs/current/man-html/net.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# net ads commands
```
net ads join [--no-dns-updates] [-U user[%pass]] [dnshostname=FQDN] [createupn=UPN] [createcomputer=OU] [machinepass=PASS] [osName=str osVer=str] [DOMAIN]
net ads leave [--keep-account]
net ads testjoin
net ads status
net ads lookup
net ads dns register [FQDN [IP ...]]
net ads dns unregister <FQDN>
net ads changetrustpw
net ads search '<LDAP expression>' <attributes...>
net ads dn '<DN>' <attributes...>
net ads setspn list|add|delete [machine] [SPN]
net ads enctypes list|set|delete <ACCOUNT$> [enctypes]
net ads keytab create
net ads keytab list [keytab]
net ads kerberos kinit [-P] [--use-krb5-ccache=CCACHE]
```
Examples:
- `net ads search '(objectCategory=group)' sAMAccountName`
- `net ads setspn add computername host/computername.example.com -U Administrator` (prompts for the password)
- `net ads enctypes set Computername$ 24 --machine-pass`

Common options: `-U`, `-S server`, `-I ip`, `-P` (machine password), `--use-kerberos=desired|required|off`, `-d 0-10`, `--json` (info, lookup). `--dns-ttl` default 3600.

Gotcha: `net ads keytab add`, `delete` and `add_update_ads` were removed in Samba 4.21; use smb.conf `sync machine password to keytab` with `net ads keytab create`.

## Checked

2026-11-04. Confirmed against the net(8) manual page: the join and leave syntax and options, testjoin, status, dns register and unregister, changetrustpw, search, dn, setspn, enctypes (list, set, delete and the examples), keytab create and list, kerberos kinit with -P and --use-krb5-ccache, the common options, --json for info and lookup, --dns-ttl default 3600, and the removal of keytab add, delete and add_update_ads in 4.21. Replaced an inline password in the setspn example.
Method: documentation only; no commands were run.
