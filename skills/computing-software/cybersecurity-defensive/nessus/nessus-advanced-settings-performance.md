---
id: computing-software.cybersecurity-defensive.nessus.nessus-advanced-settings-performance
name: nessus-advanced-settings-performance
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-deployment, nessus-advanced-settings, max-hosts, max-checks, scan-performance, network-congestion, scanner-sizing]
level: advanced
status: docs-checked
description: "Tune Nessus scan throughput safely: global vs per-scan max_hosts and max_checks, timeouts, network congestion detection, and sizing scanners for the asset count."
sources: ["https://docs.tenable.com/nessus/Content/AdvancedScanSettings.htm", "https://docs.tenable.com/general-requirements/Content/NessusScannerHardwareRequirements.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nessus advanced settings and scan performance

## Two layers
- **Scanner-level advanced settings** (Settings > Advanced): ceilings for the whole scanner, for example
  `max_hosts` and `global.max_simult_tcp_sessions` (an absolute cap across all running scans on that scanner).
- **Per-scan** (Advanced Scan template, Advanced > Performance): what one scan uses, capped by the scanner setting.
  Set "Max simultaneous hosts per scan" above the scanner's `max_hosts` and Nessus caps it at `max_hosts`
  (Tenable's example: 150 requested, `max_hosts` 100, so 100 hosts at once).

## Key knobs (Advanced Scan template defaults)
| Setting | Meaning | Default |
|---|---|---|
| Max simultaneous hosts per scan | parallel targets | 30, or the scanner `max_hosts` value if smaller |
| Max simultaneous checks per host | parallel checks per target | 5 |
| Network timeout (seconds) | wait for a host response unless a plugin says otherwise; raise on slow links | 5 |
| Slow down the scan when network congestion is detected | throttles when the network pipe nears capacity | Disabled |
| Max number of concurrent TCP sessions per host | cap on established TCP sessions; also sets SYN scanner rate at 10 packets per second per session (15 sessions = 150 pps) | none |
| Max number of concurrent TCP sessions per scan | cap for the whole scan; not enforceable in a Discovery scan | none |
| Scan targets with multiple domain names in parallel | when disabled, targets resolving to one IP are serialised | Disabled |
| Stop scanning hosts that become unresponsive | skips hosts that stop answering | Disabled |
| Scan IP addresses in a random order | spreads traffic in large scans | Disabled |

Defaults vary by template; check the template you use.

## Sizing guidance
- Tenable's minimum recommended hardware for a scanner scanning up to 50,000 hosts per scan: 4 cores at 2 GHz,
  4 GB RAM (8 GB recommended), 30 GB disk. Above 50,000 hosts per scan: 8 cores, 8 GB RAM (16 GB recommended).
  Complex and credentialed scans may need more. Read the current Scanner Hardware Requirements page.
- Nessus is CPU-intensive: avoid oversubscribed CPU in virtual machines.
- Multiple scanners near the targets beat one big scanner across a WAN.

## Tuning process
1. Baseline: run a representative subnet with defaults, record duration and errors.
2. Raise `max_hosts` in steps while watching scanner CPU/memory and target-side impact
   (firewall session tables, IDS alerts, help-desk tickets).
3. For segments with stateful firewalls or IPS in the path, cap TCP sessions; dropped sessions
   look like closed ports and cause missed findings.
4. Record the final values in the policy, not ad hoc in scans.

## Gotchas
- Too aggressive settings cause false negatives (timeouts treated as "not vulnerable"), not just
  slowness. Compare finding counts after tuning.
- Firewall session exhaustion can take down production; coordinate with network teams.
- Scanner-level settings cap what a scan asks for; check both when a scan seems slow.

## Verify
Same target set, before vs after: duration down, finding counts and credentialed-check success
unchanged, no target-side incidents.

## Checked
2026-10-31. Confirmed against the Tenable Nessus Advanced Scan Settings page and Scanner Hardware Requirements page:
defaults for max simultaneous hosts, checks per host, network timeout, congestion slow-down, TCP session caps and
the 10x packets-per-second rule, `max_hosts` capping, `global.max_simult_tcp_sessions`, hardware minimums.
Removed unconfirmed: `nessuscli fix --set` usage, `global.max_hosts`, `global.max_scans`, `checks_read_timeout`,
`plugins_timeout` and its 320 s default, "100+ on big scanners", plugin ids, and the dead SettingsPerformance source.
Method: documentation only; no commands were run.
