---
id: computing-software.systems-network-administration.network-design.honeypots-and-deception
name: honeypots-and-deception
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, segmentation, honeypot, deception-technology, canary-tokens, threat-detection]
level: practitioner
status: docs-checked
description: "Deploy honeypots, honeytokens and canaries to detect intruders inside the network: placement, realistic services, alerting, isolation and legal care."
sources:
  - https://canary.tools/help/
  - https://github.com/thinkst/opencanary
  - https://www.ncsc.gov.uk/collection/building-a-security-operations-centre/detection/detection-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Honeypots and deception

Anything touching a decoy is suspicious by definition, so deception gives high-fidelity alerts
with little tuning (deception is a recognised detection approach; see the NCSC detection practices).

## Types
| Type | Example |
|---|---|
| Low-interaction honeypot | OpenCanary (open source; optional Windows File Share and SNMP modules) and similar products emulating common services |
| High-interaction honeypot | real OS instrumented for attacker study (research, needs strong isolation) |
| Honeytokens | fake credentials, document beacons, DNS canary tokens |
| Deception platforms | decoys + breadcrumbs on endpoints at scale |

## Placement
- One or two decoys per server VLAN and user VLAN, named like real assets (`fs02`, `sql-backup`).
- Fake credentials/mapped drives on endpoints pointing to decoys.
- DMZ decoys catch scanning but generate noise; internal decoys are the high-value ones.

## Operating
- Alerts to SIEM/SOC and on-call with high priority; every alert investigated.
- Isolate decoys (no outbound internet, no trust relationships); a compromised high-interaction
  honeypot must not become a pivot.
- Exclude decoys from vulnerability scanners and asset discovery (or tag the scanner's IP) to
  avoid false alerts.
- Legal: inform legal/HR for internal monitoring policy; do not lure external attackers into
  attacking third parties.

## Verify
- [ ] Monthly test: an nmap scan or login attempt to each decoy generates an alert within minutes.

## Checked

- Date: 2026-10-28
- Confirmed: OpenCanary README: Windows File Share (Samba) and SNMP modules, Python 3.10+ prerequisites, SNMP needs Scapy. MITRE M1056 is titled Pre-compromise (proactive measures), not a deception page.
- Removed: the claim that M1056 is the deception mitigation (wrong), the M1056 source, the Thinkst Canary product claim (canary.tools returned an empty page), fake AWS key and kerberoasting detail, RDP/SSH/web login emulation list.
Method: documentation only; no commands were run.
