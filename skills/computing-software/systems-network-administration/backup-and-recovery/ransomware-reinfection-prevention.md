---
id: computing-software.systems-network-administration.backup-and-recovery.ransomware-reinfection-prevention
name: ransomware-reinfection-prevention
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [reinfection-prevention, ransomware-recovery, hardening, persistence-removal, staged-reconnection, incident-response]
level: advanced
status: draft
description: "Harden before reconnecting restored systems after ransomware: close the entry point, remove persistence, reset credentials, EDR coverage, staged reconnection and monitoring."
sources:
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://csrc.nist.gov/pubs/sp/800/61/r3/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preventing reinfection before reconnecting

**Goal:** restored systems go back online without the attacker walking straight back in.

## Close the way in
- Identify initial access from the IR investigation (phished credentials, exposed RDP/VPN without MFA, unpatched edge device, supplier access).
- Patch or replace the exploited system; enforce MFA on all remote access; remove internet-exposed RDP/SMB; rotate VPN and appliance credentials and certificates.

## Remove persistence
Hunt and remove across restored and surviving hosts: new local/domain accounts, scheduled tasks, services, Run keys, WMI subscriptions, malicious GPOs and logon scripts, remote tools (AnyDesk, ScreenConnect), web shells, and modified firewall rules. Use the IR team's IOC list and YARA rules.

## Credentials
- Reset all privileged accounts, service accounts, and then all users; reset krbtgt twice (with replication in between); rotate API keys, cloud tokens and secrets stored on compromised hosts.
- Revoke sessions and refresh tokens in the IdP.

## Rebuild order and staged reconnection
1. Clean network segment with EDR, logging and egress filtering in place.
2. Identity first (clean or rebuilt DCs), then core infrastructure, then apps by BIA priority.
3. Each system: restored from a point before initial access, patched, EDR installed and healthy, scanned, then moved into production VLAN.
4. Block known C2 domains/IPs at firewall and DNS.

## Heightened monitoring
30-90 days of increased alerting sensitivity and threat hunting; watch for the known TTPs and any reuse of reset accounts.

## Gotchas
- Reconnecting a single uncleaned host (a forgotten jump box or a laptop back from leave) re-seeds the attack.
- Restoring images that contain the attacker's tools from the dwell period.

## Verify
Go-live checklist per system signed off by security: patched, EDR reporting, no IOCs, credentials rotated; at the end, an independent compromise assessment.
