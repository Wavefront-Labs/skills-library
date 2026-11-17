---
id: computing-software.systems-network-administration.active-directory.rename-domain-joined-servers-and-dcs
name: rename-domain-joined-servers-and-dcs
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, domain-join, netdom-computername, rename-computer, domain-controller]
level: practitioner
status: docs-checked
description: "Rename member servers with Rename-Computer and domain controllers with netdom computername add/makeprimary/remove, keeping SPNs and DNS correct."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netdom-computername
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/rename-computer
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setspn
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Renaming domain-joined servers and DCs

## Member server
```powershell
Rename-Computer -NewName APP02 -DomainCredential CORP\joiner -Restart
```
Explicit credentials (`-DomainCredential`) are required to rename a computer that is joined to a domain. Before
renaming:
- Check custom SPNs on the computer account (`setspn -L APP01`), app configs, DNS CNAMEs, certificates with the old
  name, monitoring, backup jobs. Update any SPN or DNS record that references the old name.
- Check whether the server's roles tolerate a rename (for example certification authorities, Exchange and cluster
  nodes) against the vendor's documentation first.

## Domain controller (no demotion needed)
Use the alternate-name method so clients keep working during the switch:
```cmd
netdom computername dc01.corp.example.com /add:dc11.corp.example.com
:: wait for replication of the new SPN and DNS registration
netdom computername dc01.corp.example.com /makeprimary:dc11.corp.example.com
shutdown /r /t 0
:: after reboot and replication
netdom computername dc11.corp.example.com /remove:dc01.corp.example.com
```
- `/add` creates an alternate DNS name, `/makeprimary` promotes an alternate name to primary, `/remove` deletes an
  alternate name, and `/verify` checks that each computer name has a DNS record and an SPN.
- Wait for `repadmin /syncall` and `dcdiag /test:dns` between steps.
- Clients and apps pinned to the old DC name (LDAP binds in apps, DNS forwarders on appliances) must be updated before
  `/remove`.

## Verify
- [ ] `nltest /dsgetdc:corp.example.com /server:<newname>` works.
- [ ] `netdom computername <newname> /verify` reports DNS records and SPNs for each name; `setspn -X` shows no
  duplicate SPNs.
- [ ] `repadmin /showrepl` healthy for the renamed DC.

## Checked

Date: 2026-10-27. Documentation: netdom computername reference, Rename-Computer module page, setspn reference,
repadmin and nltest references (MicrosoftDocs repositories, main branch).
Confirmed: `netdom computername` `/add`, `/makeprimary`, `/remove`, `/verify` meanings, the `-DomainCredential` need and
parameters of Rename-Computer, `setspn -L` and `-X`, `repadmin /syncall`, `dcdiag /test:dns`, `nltest /dsgetdc`.
Removed unconfirmed claims: that Rename-Computer rewrites `dNSHostName` and default SPNs, the "domain functional level
2003+" requirement, and specific role blockers such as AD CS name binding.

Method: documentation only; no commands were run.
