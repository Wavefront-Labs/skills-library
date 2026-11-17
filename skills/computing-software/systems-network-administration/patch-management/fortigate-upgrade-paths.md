---
id: computing-software.systems-network-administration.patch-management.fortigate-upgrade-paths
name: fortigate-upgrade-paths
category: computing-software
field: systems-network-administration
product: patch-management
tags: [fortigate-upgrade-path, fortinet, fortios, firewall-upgrade, network-device-patching, patch-management]
level: practitioner
status: docs-checked
description: "Upgrade FortiGate firewalls along Fortinet's validated upgrade path with the Upgrade Path Tool: hop-by-hop planning, backups, release notes and post-upgrade checks."
sources:
  - https://docs.fortinet.com/upgrade-tool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FortiGate upgrade paths

Fortinet QA validates specific point-to-point FortiOS upgrades. Follow the validated path hop by hop rather than jumping straight to the target.

## Plan the path
1. Fortinet Upgrade Path Tool (docs.fortinet.com/upgrade-tool): choose the product and model, the current version and the target version. It returns the shortest tested path. Other paths may work, but only the shortest validated one is shown.
2. Read the release notes for every hop: upgrade information, special notices, changes in default behavior, known issues. Some versions have prerequisites.
3. Back up the current configuration and the licence file before the first hop.

## Upgrade
- Each step is a full install of that firmware build. Wait for services to stabilise between hops; do not skip ahead.
- HA clusters: follow Fortinet's documented HA upgrade procedure for your FortiOS version (administration guide and release notes).
- Before the first hop, record a baseline you can compare against afterwards: sessions, VPN tunnels, routing neighbours, policy count.

## Gotchas
- Release notes list removed or restricted features and changed defaults; check each hop and diff the configuration before and after.
- A path that works for one model may not exist for another: always run the tool for the exact model.

## Verify
The running version equals the target, and tunnels, routing and sessions are back to the recorded baseline.

## Checked
2026-10-28. Confirmed against the Fortinet Upgrade Path Tool page (shortest tested path, only validated path shown, each hop a full install, release notes sections, back up configuration and licence, follow the documented HA procedure). Removed: example version path, CLI commands (`execute federated-upgrade`, `execute restore image`, `diagnose sys ha checksum cluster`, flash partition rollback), the 7.2.4 GUI claim, SSL VPN and FortiManager notes, and the two administration guide sources, whose fetched pages covered other topics.
Method: documentation only; no commands were run.
