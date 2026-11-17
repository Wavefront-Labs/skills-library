---
id: computing-software.systems-network-administration.samba.bind9-dlz-backend
name: bind9-dlz-backend
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, bind9-dlz-backend, bind9-dlz, samba-upgradedns, dlz, bind]
level: advanced
status: docs-checked
description: "Use BIND9 with the Samba DLZ module as AD DNS: provisioning option, named.conf include, module per BIND version, keytab settings, restart-only rule."
sources:
  - https://wiki.samba.org/index.php/BIND9_DLZ_DNS_Back_End
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bind9 dlz backend
The `bind-dns` directory is created when you provision, join or upgrade with `--dns-backend=BIND9_DLZ`. To switch an existing DC: `samba_upgradedns --dns-backend=BIND9_DLZ`.

named.conf include (Samba 4.7 and earlier used the `private/` path):
`include "/usr/local/samba/bind-dns/named.conf";`

Pick the DLZ module matching `named -v` by uncommenting its line in that file (default is the 9.11 module):
```
dlz "AD DNS Zone" {
    database "dlopen /usr/local/samba/lib/bind9/dlz_bind9_11.so";
};
```
Other modules: `dlz_bind9.so` (9.8), `dlz_bind9_9.so`, `dlz_bind9_10.so`, `dlz_bind9_12.so`, `dlz_bind9_14.so`, `dlz_bind9_16.so`.

Options block:
```
options {
    tkey-gssapi-keytab "/usr/local/samba/private/dns.keytab";
    minimal-responses yes;
};
```
Permissions: pre-4.4.0 `chmod 640` and `chown root:named` the keytab; upgrades from before 4.8.0 need `chmod 770` and `chown root:named` on `bind-dns`. BIND must read `/etc/krb5.conf`; `nsupdate` must exist.

Check with `named-checkconf`. Dynamic updates need BIND 9.8+.

Gotcha: you cannot `reload` BIND on a Samba DC, only restart. Add `-d 3` to the `database` line for DLZ debug output.

## Checked

2026-11-04. Confirmed against the Samba wiki page BIND9 DLZ DNS Back End: bind-dns directory and 4.8.0 path change, DLZ module per BIND version, 9.8 minimum for dynamic updates, keytab permission fixes (pre-4.4.0, pre-4.8.0), nsupdate requirement, restart-only rule, and the -d 3 debug option.
Method: documentation only; no commands were run.
