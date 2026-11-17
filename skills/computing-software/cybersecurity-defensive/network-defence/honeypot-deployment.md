---
id: computing-software.cybersecurity-defensive.network-defence.honeypot-deployment
name: honeypot-deployment
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [deception-technology, honeypot, opencanary, t-pot, internal-honeypot, high-interaction-honeypot, low-interaction-honeypot, lateral-movement-detection]
level: practitioner
status: draft
description: "Deploy internal honeypots (OpenCanary, T-Pot, commercial decoys) that produce high-fidelity alerts on lateral movement and scanning, with safe placement and alert routing."
sources: ["CompTIA Security+ SY0-701 objective 1.2 (honeypot, honeynet)", "MITRE D3FEND Decoy Environment (D3-DE)", "OpenCanary documentation (Thinkst)", "T-Pot documentation (Deutsche Telekom Security)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Honeypot deployment

**Goal:** decoy systems that no legitimate user should ever touch, so any interaction is a
high-confidence signal of scanning or lateral movement.

## Internal vs internet-facing
- **Internal honeypots** (inside the network): best value for defenders; almost zero false positives.
- **Internet-facing** (T-Pot and similar): research and threat intelligence on mass exploitation; noisy, not for alerting.

## OpenCanary (low interaction, internal)
```
pip install opencanary
opencanaryd --copyconfig        # creates /etc/opencanaryd/opencanary.conf
```
Enable a believable set of services in the JSON config, e.g. SMB (with Samba), RDP, SSH,
HTTP login page, MSSQL, with banners matching a real OS version, and set
`"device.node_id": "FILESRV-BAK02"`. Output via syslog/webhook to the SIEM.
`opencanaryd --start`.
Commercial options (Thinkst Canary, Zscaler Deception, Attivo/SentinelOne) add easy management and realistic personas.

## Placement and realism
- One or more per significant subnet (server VLANs, user VLANs, DMZ, OT boundary).
- Names that fit the naming convention and look valuable (`backup`, `sql`, `finance-files`).
- Register in DNS and AD (as a computer object) so attackers enumerating find it.
- No production data; isolated so a compromised honeypot cannot pivot (high interaction ones especially).

## Alerting
- Any connection = alert. Route straight to the SOC with high priority, including source host and service touched.
- Exclude your own vulnerability scanners and asset discovery by source IP, and document it (attackers love scanner IPs - consider a separate alert when scanner IPs touch the canary outside scan windows).

## Gotchas
- Default banners and hostnames are fingerprinted by attackers; customise them.
- Forgotten honeypots become unpatched real hosts: patch and monitor them like any server.
- Legal/privacy: internal monitoring is generally fine; internet honeypots that are compromised could be used to attack others - isolate and rate-limit egress.

## Verify
- [ ] A port scan from a test host triggers an alert in the SIEM within minutes.
- [ ] Inventory of decoys with owner and last test date.
