---
id: computing-software.systems-network-administration.cisco-networking.cis-benchmark-ios-configuration-audit
name: cis-benchmark-ios-configuration-audit
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, cis-benchmark, configuration-audit, device-hardening, compliance, nipper, batfish, security-baseline]
level: practitioner
status: draft
description: "Audit IOS/IOS XE configs against the CIS Cisco IOS Benchmark: key controls by plane, automated checking with show commands or tools, and handling exceptions."
sources:
  - https://www.cisecurity.org/benchmark/cisco
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CIS benchmark configuration audit

## The benchmark
CIS publishes Cisco IOS and IOS XE benchmarks (free PDF with registration). Controls are grouped
by management, control and data plane, each with audit (`show run | include ...`) and remediation
commands. Level 1 = baseline for everyone; Level 2 = higher security, may affect operations.

## High-value controls (Level 1 examples)
| Plane | Control | Audit |
|---|---|---|
| Management | `aaa new-model`, AAA login/exec/accounting | `show run | inc aaa` |
| Management | SSH v2 only, VTY `transport input ssh`, `access-class` | `show ip ssh`, `show run | sec line vty` |
| Management | `exec-timeout` <= 10 min on all lines | `show run | sec line` |
| Management | `enable secret` (type 8/9), no `enable password` | `show run | inc enable` |
| Management | `service password-encryption`, no type 7 for users | `show run | inc username` |
| Management | SNMPv3 authPriv, no `public`/`private` communities | `show snmp community`, `show snmp user` |
| Management | Login banner set | `show run | beg banner` |
| Management | Logging to remote host with timestamps, NTP authenticated | `show run | inc logging|ntp` |
| Control | Routing protocol authentication (OSPF/EIGRP/BGP) | per protocol |
| Data | `no ip source-route`, `no ip proxy-arp`, uRPF on edge | `show run | inc source-route` |
| Services | `no ip http server`, no CDP on edge, `no service pad`, no small servers | `show run | inc http|cdp|pad` |

## Automating the audit
- Collect configs (Oxidized/RANCID/Ansible `ios_facts`), then check with:
  - Ansible playbooks with `ios_command` + asserts, or `cisco.ios.ios_config` in check mode.
  - Batfish (`bf.q.nodeProperties`, custom assertions) or pyATS/Genie parsers.
  - Commercial: Titania Nipper, Tenable/Nessus compliance audits (CIS .audit files), Catalyst Center compliance.
- Output a per-device pass/fail per control ID, tracked over time.

## Exceptions
Document deviations (e.g. HTTP server needed for RESTCONF, CDP needed for phones) with control ID,
justification, compensating control and review date. An audit with unexplained exceptions is noise.

## Verify
- [ ] Scheduled audit runs weekly; new failures alert; exceptions register reviewed quarterly.
