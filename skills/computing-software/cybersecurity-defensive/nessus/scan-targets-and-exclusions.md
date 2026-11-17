---
id: computing-software.cybersecurity-defensive.nessus.scan-targets-and-exclusions
name: scan-targets-and-exclusions
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-policy, scan-exclusions, target-lists, rules-file, exclusion-windows, tenable-vulnerability-management, scope-management]
level: practitioner
status: draft
description: "Define Nessus/Tenable scan targets and exclusions: target syntax, upload files, scanner-wide rules (reject), Tenable VM exclusions with schedules, and keeping scope current."
sources: ["https://docs.tenable.com/nessus/Content/ScanTargets.htm", "https://docs.tenable.com/nessus/Content/AdvancedSettings.htm", "https://docs.tenable.com/vulnerability-management/Content/Settings/exclusions/Exclusions.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scan targets and exclusions

## Target syntax
- Single IP `10.1.2.3`, range `10.1.2.10-10.1.2.50`, CIDR `10.1.0.0/16`, hostname `web01.corp`,
  IPv6 addresses, and `hostname[ip]` to scan an IP but report the hostname (useful for virtual hosts).
- Upload a text file of targets (one per line) for large lists; keep the file generated from the
  CMDB/IPAM rather than hand-edited.
- Hostnames are resolved at scan time; stale DNS means scanning the wrong box.

## Exclusion mechanisms
1. **Scanner rules (Nessus)**: Settings > Advanced > `rules` file path, or `nessusd.rules` in the
   config dir:
   ```
   reject 10.1.5.0/24     # OT segment, never scan from this scanner
   reject 10.1.2.15
   default accept
   ```
   Applies to every scan on that scanner: the safety net for "never touch" systems.
2. **Tenable Vulnerability Management exclusions**: Settings > Exclusions; IP/range/host with an
   optional recurring schedule (e.g. no scanning payroll servers on the last business day).
   Applies to network scans across cloud scanners and linked Nessus scanners (not agents).
3. **Tenable Security Center**: blackout windows and repository-scoped scan zones.
4. **Per scan**: simply leave targets out; least reliable because each scan owner must remember.

## What usually belongs on the exclusion list
- Fragile devices: PLCs, medical devices, old printers, VoIP gear (scan them with a separate,
  gentle policy if at all).
- Third-party-owned or customer systems you have no authority to scan.
- Systems under change freeze during specific windows (schedule-based exclusions).

## Keep it honest
- Every exclusion needs an owner, reason and review date; excluded hosts are unmeasured risk.
- Report excluded asset counts in coverage metrics.
- Prefer agent-based assessment for excluded hosts where possible.

## Gotchas
- Scanner `rules` are per scanner; a scan routed to a different scanner ignores them. Use
  platform-level exclusions for anything critical.
- Exclusions by IP do not follow DHCP hosts; use hostnames or asset tags where supported.
- Scanner `reject` rules stop that scanner from sending any traffic to the IP, but other scanners,
  agents' network checks or discovery tools may still reach it.

## Verify
After a scan, check the scan's host list: excluded IPs must not appear, and the scanner log
(`nessusd.messages`) shows "rejected" entries for them.
