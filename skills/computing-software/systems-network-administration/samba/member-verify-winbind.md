---
id: computing-software.systems-network-administration.samba.member-verify-winbind
name: member-verify-winbind
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, member-verify-winbind, getent, member-troubleshooting, winbind, wbinfo]
level: practitioner
status: docs-checked
description: "Verify and troubleshoot a Samba domain member's winbind: ping-dc, getent lookups, empty enumeration, default-domain names, loopback net failures."
sources:
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_a_Domain_Member
  - https://wiki.samba.org/index.php/Troubleshooting_Samba_Domain_Members
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# member verify winbind
Checks:
```
wbinfo --ping-dc
getent passwd "SAMDOM\demo01"
getent group "SAMDOM\Domain Users"
chown "SAMDOM\demo01:SAMDOM\domain users" file.txt
```
Fixes:
- `getent passwd` lists no domain users: expected by default. `winbind enum users = yes` and `winbind enum groups = yes` change that, but slow lookups; use for testing only.
- `getent passwd demo01` fails but `getent passwd "SAMDOM\demo01"` works: set `winbind use default domain = yes`.
- Individual lookups work but not full lists: confirm `libnss_winbind` is usable, then enable the two enum options and `smbcontrol all reload-config`.
- `net rpc rights list -U administrator` gives `NT_STATUS_CONNECTION_REFUSED`: make Samba listen on loopback, or pass `-I IP` / `-S host`.
- `ERROR_DNS_UPDATE_FAILED` on join: check dynamic DNS on the DC.
- `ERROR_DNS_GSS_ERROR`: Kerberos problem on a BIND9_DLZ DC.

Log level 3 or higher in `[global]` exposes errors such as `Server exit (NT_STATUS_CONNECTION_RESET)` caused by an `includedir` in krb5.conf; remove that line.

## Checked

2026-11-04. Confirmed against the Samba wiki pages Setting up Samba as a Domain Member and Troubleshooting Samba Domain Members: wbinfo --ping-dc, getent and chown checks, winbind enum options and their slowness, winbind use default domain, libnss_winbind check and reload-config, NT_STATUS_CONNECTION_REFUSED with -I/-S, the two DNS update errors, log level 3 includedir failure. Removed the unconfirmed `net cache flush` stale-ID line.
Method: documentation only; no commands were run.
