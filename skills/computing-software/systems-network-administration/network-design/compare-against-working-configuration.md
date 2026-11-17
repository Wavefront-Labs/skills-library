---
id: computing-software.systems-network-administration.network-design.compare-against-working-configuration
name: compare-against-working-configuration
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-methodology, compare-configurations, spot-the-difference, config-diff, config-backup]
level: practitioner
status: docs-checked
description: "Troubleshoot by comparing a failing device, port or site against a known-good one: config backups and diffs, normalising noise, show-output comparisons and change history."
sources:
  - https://github.com/ytti/oxidized
  - https://www.comptia.org/certifications/network
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compare against a working configuration

When one site/switch/port fails and a near-identical one works, the difference is usually the cause.

## Sources of "known good"
- The same device yesterday: config backups (Oxidized, which can store configs in git, or RANCID, or
  the vendor's config archive feature, or a Golden Config tool).
- A sibling device/site built from the same template.
- The golden/intended config rendered from the source of truth.

## Diffing
```
diff -u good.cfg bad.cfg
git -C oxidized-repo log -p --since=2.days -- sw-lon1-as03      # what changed recently
```
Most platforms can diff the running config against an archived or rolled-back one; use the vendor's
compare command. Normalise noise first: timestamps, crypto hashes, certificate blobs, interface
numbering if comparing different hardware, order of unordered sections.

## Beyond config
Diff operational state too: software version, interface status, LLDP neighbours, routing table
summaries, licences, transceiver types. Many "identical" sites differ in firmware or optic.

## Port-level spot the difference
Working vs failing access port: compare the interface configuration, switchport/VLAN state,
authentication session state, PoE class and speed/duplex.

## Verify
- [ ] The incident record names the specific difference found, why it caused the fault, and the template/backup check that would catch it next time.

## Checked

2026-10-28: Confirmed: Oxidized README (configuration backup tool, RANCID replacement, git output module), diff -u (GNU diff man page), git log --since (git docs). Removed: the sed noise filter, the IOS archive path and write-memory, show archive config differences, Junos compare rollback and the vendor show command list; the Cisco rollback source was a 404.
Method: documentation only; no commands were run.
