---
id: computing-software.systems-network-administration.cisco-networking.vtp-revision-number-risk
name: vtp-revision-number-risk
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, vtp, vtp-revision-number, vtp-transparent, vlan-database, change-safety]
level: practitioner
status: draft
description: "Stop a newly connected switch from wiping every VLAN via VTP: check and reset the configuration revision, use transparent/off or VTPv3 primary server, and recover."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/vtp/10558-21.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/vlan/b_179_vlan_9300_cg/configuring_vtp.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VTP revision number risk

VTPv1/v2 trusts the highest configuration revision in the domain. A lab switch with the same domain
name and a higher revision, plugged in as server or client, overwrites the VLAN database of every
switch. Ports in deleted VLANs go inactive: an instant outage.

## Before connecting any switch
```
show vtp status
!  VTP Operating Mode : Server
!  VTP Domain Name    : CORP
!  Configuration Revision : 47
```
Reset the revision to 0 on the new switch, any one of:
```
vtp mode transparent        ! revision resets to 0
vtp mode client             ! or back to the mode you need
! or
vtp domain RESET-TEMP
vtp domain CORP
```
Then confirm `Configuration Revision : 0` before cabling the trunk.

## Safer designs
- `vtp mode transparent` everywhere (VLANs configured per switch, kept in running-config).
- `vtp mode off` (VTPv3 or newer releases): no VTP processing at all.
- VTPv3: only the designated primary server can push changes, so a rogue revision is ignored.
  ```
  vtp version 3
  vtp domain CORP
  vtp password S3cret hidden
  vtp mode server
  vtp primary vlan force       ! exec command, on the one switch allowed to make changes
  ```

## Recovery after a wipe
1. Disconnect the offending switch.
2. On the switch that holds the true config (or from your last backup of `vlan.dat` / running
   config of transparent switches), recreate the VLANs with names.
3. With the revision now highest on the good server, clients resync automatically.
4. Restore pruning and private VLAN settings if used.

## Gotchas
- `vlan.dat` lives in flash, not in running-config, for server/client modes. Back it up
  (`copy flash:vlan.dat tftp:`) or document VLANs in a source of truth.
- A VTP password mismatch causes `MD5 digest checksum mismatch` and silent non-sync, not a wipe.
- Extended VLANs (1006-4094) need VTPv3 or transparent mode.

## Verify
- [ ] Every switch shows the expected mode and the same revision (server/client) or 0 (transparent).
- [ ] `show vlan brief` identical across the domain after any change.
