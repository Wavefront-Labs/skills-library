---
id: computing-software.systems-network-administration.samba.join-additional-dc
name: join-additional-dc
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, join-additional-dc, domain-join, second-dc, active-directory, samba-tool]
level: practitioner
status: docs-checked
description: "Join a further Samba DC to an existing AD domain with samba-tool domain join, including DNS forwarder, site and interface options, and post-join checks."
sources:
  - https://wiki.samba.org/index.php/Joining_a_Samba_DC_to_an_Existing_Active_Directory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# join additional dc
Prerequisites: synchronised time, first nameserver in `/etc/resolv.conf` pointing at an existing DC, and `/etc/krb5.conf` with `default_realm`, `dns_lookup_realm = false`, `dns_lookup_kdc = true`. Confirm with `kinit administrator` and `klist`.

Join (pick one authentication form):
```
samba-tool domain join samdom.example.com DC -U"SAMDOM\administrator"
samba-tool domain join samdom.example.com DC -k yes
samba-tool domain join samdom.example.com DC --use-krb5-ccache=/tmp/krb5cc_0
```
Options:
- `--dns-backend=SAMBA_INTERNAL` or `BIND9_DLZ`.
- `--option="dns forwarder=IP"` (required with internal DNS; you are not prompted).
- `--site=SITE` to join a given AD site.
- `--option="interfaces=lo eth0" --option="bind interfaces only=yes"`.
- `--option='idmap_ldb:use rfc2307 = yes'` if other DCs used `--use-rfc2307`.

Then start `samba`. Samba 4.7+ creates initial DNS entries during the join.

Checks: `samba-tool drs showrepl` (DomainDnsZones and ForestDnsZones inbound OK; KCC can take up to 15 minutes), `host -t A samdom.example.com localhost` lists all DCs.

Sysvol: Samba has no built-in replication; use an rsync or Robocopy workaround, then `samba-tool ntacl sysvolreset`. Copy `idmap.ldb` from the DC holding the PDC emulator role (hot backup with `tdbbackup -s .bak`) and run `net cache flush` on the new DC.

## Checked

2026-11-04. Confirmed against the Samba wiki page Joining a Samba DC to an Existing Active Directory: krb5.conf settings, kinit/klist, the three join forms, --dns-backend values, dns forwarder requirement with the internal DNS, --site, interfaces options, rfc2307 idmap option, 4.7 initial DNS entries, 15 minute KCC delay, host -t A check, sysvol workarounds (rsync, Robocopy), sysvolreset, idmap.ldb sync with tdbbackup and net cache flush.
Method: documentation only; no commands were run.
