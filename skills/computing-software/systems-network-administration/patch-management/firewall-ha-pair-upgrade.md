---
id: computing-software.systems-network-administration.patch-management.firewall-ha-pair-upgrade
name: firewall-ha-pair-upgrade
category: computing-software
field: systems-network-administration
product: patch-management
tags: [network-device-upgrade, appliance-patching, ha-pair-upgrade, firewall-upgrade, active-passive, session-sync, upgrade-path, patch-management]
level: advanced
status: draft
description: "Upgrade an active/passive firewall HA pair with minimal disruption: upgrade path checks, config backup, passive first, failover, upgrade the other, session sync caveats and rollback."
sources:
  - https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading a firewall HA pair

**Goal:** patch perimeter firewalls (often under emergency advisories) while traffic keeps
flowing, with a tested way back.

## Prepare
- **Upgrade path:** vendors require intermediate versions (feature release boundaries,
  base images). Check the vendor upgrade path tool/release notes; download all images and
  verify hashes.
- **Compatibility:** content/threat signature versions, VPN client versions, management
  server (Panorama, FortiManager) must be same or newer than devices.
- **Backups:** export running configuration and device state from both units; note
  licences and HA status.
- **Window and comms:** even "hitless" upgrades drop some sessions (failover, asymmetric
  flows, VPNs renegotiate).
- Disable preemption during the upgrade so units don't flip unexpectedly.

## Sequence (active/passive)
1. Confirm HA healthy and config synced.
2. Upgrade the **passive** unit; reboot; verify version and that it rejoins HA as passive
   (HA may report version mismatch: expected during the upgrade).
3. **Fail over** (suspend the active unit or trigger manual failover); the upgraded unit
   becomes active. Test: internet access, VPNs, key apps, NAT, logs flowing.
4. Upgrade the original active unit (now passive); reboot; rejoin.
5. Re-enable preemption if used; optionally fail back.

FortiGate "uninterruptible upgrade" automates this order for clusters; Palo Alto requires
manual per-unit steps; Cisco FTD via FMC upgrades HA pairs in sequence.

## Rollback
Most appliances keep the previous image in a second partition: boot the old image on the
upgraded unit (it may need the config backup from that version). Know the vendor-specific
rollback command before you start.

## Gotchas
- Mismatched versions in HA usually block config sync: don't stay in that state.
- Emergency advisories sometimes ship hotfix builds with their own paths; read the advisory.
- After a CVE affecting management planes, also rotate admin credentials and check for
  indicators of compromise; patching alone may be insufficient.

## Verify
Both units show the target version, HA state healthy and in sync, session table and VPN
tunnels up, monitoring shows no traffic drop beyond the failover blip.
