---
id: computing-software.systems-network-administration.network-design.configuration-compliance-checks
name: configuration-compliance-checks
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, documentation, config-compliance, golden-config, batfish, audit]
level: practitioner
status: docs-checked
description: "Check network device configurations against a golden standard: rule definitions, tools (Batfish, Oxidized + scripts, NetBox/Nautobot Golden Config, vendor tools), and remediation."
sources:
  - https://batfish.readthedocs.io/en/latest/
  - https://docs.nautobot.com/projects/golden-config/en/latest/
  - https://www.cisecurity.org/benchmark/cisco
  - https://github.com/ytti/oxidized
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration compliance checks

## Define the standard
- Golden config snippets per role/platform: AAA, NTP, logging, SNMPv3, banners, SSH-only, disabled
  services, management ACLs, STP guards on access ports, QoS templates.
- Security baselines: CIS Benchmarks for Cisco devices (free PDF for non-commercial use), vendor hardening guides.
- Express rules as **must contain**, **must not contain**, and **parsed value checks**
  (e.g. every access port has BPDU guard enabled).

## Tools
| Tool | Approach |
|---|---|
| Nautobot Golden Config app | golden configuration and configuration compliance |
| Batfish | analyses uploaded device configurations offline by running questions (see its question catalogue) |
| Oxidized/RANCID + scripts | config backups (Oxidized can output to git); your own checks per rule |

## Process
1. Nightly backup -> compliance run -> report per device and rule.
2. Exceptions recorded with expiry and approver.
3. Remediation through change management, ideally automated push of the missing snippet.
4. Trend compliance % per site over time.

## Verify
- [ ] Compliance report runs automatically, covers 100 % of devices in inventory, and non-compliant items have tickets or approved exceptions.

## Checked

- Date: 2026-10-28
- Confirmed: Nautobot Golden Config: app for golden configuration and configuration compliance; Oxidized: network device config backup tool, RANCID replacement, git output module; Batfish: question-based analysis of uploaded configs; CIS Cisco benchmark: free PDF for non-commercial use.
- Removed: DISA STIG reference, vendor compliance products, ciscoconfparse code example, Batfish query list, NetBox config template claim.
Method: documentation only; no commands were run.
