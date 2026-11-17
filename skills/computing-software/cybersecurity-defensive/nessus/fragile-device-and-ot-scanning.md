---
id: computing-software.cybersecurity-defensive.nessus.fragile-device-and-ot-scanning
name: fragile-device-and-ot-scanning
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-policy, fragile-device-scanning, ot-security, safe-checks, printers, ics-scanning, tenable-ot-security, passive-scanning]
level: advanced
status: draft
description: "Scan fragile and OT devices without breaking them: Nessus fragile-device settings, low-concurrency safe policies, passive alternatives, change approval and rollback plans."
sources: ["https://docs.tenable.com/nessus/Content/ScanSettingsReference.htm", "https://www.cisa.gov/resources-tools/resources/primary-mitigations-reduce-cyber-threats-operational-technology", "https://docs.tenable.com/ot-security/Content/Home.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scanning fragile and OT devices

Active scans have crashed PLCs, infusion pumps, printers and old network gear. The rule is:
discover passively first, scan actively only with owner approval and a gentle policy.

## Nessus built-in protection
Policy > Discovery > Fragile Devices:
- "Scan Network Printers" and "Scan Novell Netware hosts" are **off** by default: leave them off
  in general policies. Printers otherwise receive data on port 9100 and print garbage pages.
- "Scan Operational Technology devices" is off by default: when off, Nessus skips hosts it
  identifies as OT during discovery.
Safe checks (Assessment > General > "Perform thorough tests" off, Advanced "Safe checks" on) avoid
plugins known to be disruptive. Never run "denial of service" plugin families on OT.

## Gentle active policy for approved OT scans
- Max simultaneous hosts 1-5, checks per host 1, TCP sessions per host 2-4.
- Ping only with ICMP/ARP; port scan a small known port list (e.g. 102, 502, 20000, 44818, 47808,
  80, 443) instead of all ports; disable UDP scanning unless required.
- Disable web application tests and brute-force families.
- Credentialed checks against Windows-based HMIs/historians are lower risk than probing the
  controllers themselves.

## Passive and native options first
- Passive network monitoring (Tenable OT Security, Nozomi, Claroty, Dragos, Zeek with ICS parsers)
  identifies assets, firmware versions and vulnerabilities from traffic.
- Vendor/ICS-protocol queries (Tenable OT "active queries" speak native protocols at low rates).
- Asset owner exports (engineering workstation project files list firmware versions).

## Process
1. Inventory and classify: which devices are safety-critical, which are fragile IT (printers, VoIP).
2. Change request with plant/clinical owner; scan during maintenance window; operator on site.
3. Test the policy against a spare/lab unit of the same model first.
4. Rollback plan: how to power-cycle or restore the device; vendor contacts.
5. Record results; schedule rescans at the same cadence as maintenance windows, not weekly.

## Gotchas
- Discovery alone (ping sweep, SYN scan) can disrupt some devices; exclusion rules at scanner level
  are the safety net (see scanner `reject` rules).
- Scanner placement: traffic crossing OT firewalls may be blocked or alarmed; coordinate.
- IT policies "inherited" into OT scans are the usual cause of incidents.

## Verify
Device health checks (HMI status, process values, device logs) before, during and after; no
alarms in the control system; scan completes with expected assets.
