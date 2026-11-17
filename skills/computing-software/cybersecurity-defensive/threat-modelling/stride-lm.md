---
id: computing-software.cybersecurity-defensive.threat-modelling.stride-lm
name: stride-lm
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [stride-lm, stride, lateral-movement, threat-modelling, lockheed-martin]
level: practitioner
status: docs-checked
description: "Apply STRIDE-LM, Lockheed Martin's STRIDE plus Lateral Movement categorisation, to name effect, security property and control type for each threat."
sources: ["https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/cyber/LM-White-Paper-Threat-Driven-Approach.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STRIDE-LM

Lockheed Martin's 2019 white paper on a threat-driven approach adds one threat type,
**Lateral Movement (LM)**, to Microsoft's STRIDE. STRIDE is primarily focused on software
engineering and development, so lateral movement, which is primarily a system-of-systems
threat, was not included. The LM addition follows the pattern of describing the effect of a
threat.

## Table 1: category, property, controls (paper)
| Threat | Property | Default control types |
|---|---|---|
| Spoofing: impersonating someone or something | Authentication | Authentication stores, strong authentication mechanisms |
| Tampering: modifying data or code | Integrity / access controls | Crypto hash, digital watermark, isolation and access checks |
| Repudiation: claiming not to have performed an action | Non-repudiation | Logging infrastructure, full packet capture |
| Information disclosure: exposing data to unauthorised parties | Confidentiality | Encryption or isolation |
| Denial of service: deny or degrade service | Availability | Redundancy, failover, QoS, bandwidth throttle |
| Elevation of privilege: gain capabilities without proper authorisation | Authorisation / least privilege | RBAC, DACL, MAC; sudo, UAC, privileged account protections |
| Lateral movement: expand influence after compromise, often dependent on elevation of privilege | Segmentation / least privilege | Credential hardening; segmentation and boundary enforcement; host-based firewalls |

The threat model identifies primary threat types, each of which references a security property
and a control type. The paper ties these default controls to its Functional Controls
Hierarchy.

## How the paper uses it
- A threat model shows four things: the assets, the attack surface, how components and assets
  interact, and the threat actors and how an attack could occur (the paper's IDDIL/ATC
  methodology).
- The paper does not advocate one technique, tool or taxonomy; each team should choose what
  fits its mission.
- Worked example: extraction of Windows password hashes from memory. The primary threat is
  information disclosure of the hashes; elevation of privilege and lateral movement are
  resultant threats. The paper notes the threat is relatively constant over time while risk
  varies with attacker tooling and protections.
- The paper treats lateral movement as one of the largest threats and cites Windows
  pass-the-hash as a primary mechanism, corresponding to the actions-on-objectives step of the
  kill chain.

## Using it in a model
1. Run STRIDE on each element as usual.
2. Add the LM category: for each element, state which resultant threats follow if it is
   compromised (as in the hash example, disclosure leads to elevation and lateral movement).
3. For each threat, record the property and control type from Table 1.

## Verify
- [ ] Every high threat names its primary threat type and any resultant lateral movement.
- [ ] Each has a control type taken from the Table 1 column for its category.

## Checked
Confirmed 2026-11-09 against the Lockheed Martin white paper (pdftotext, the categorisation section, Table 1, the focus-on-largest-threats section and the password hash worked example read).
Removed as unconfirmed: the zone-based DFD procedure, credential and protocol enumeration questions, ATT&CK TA0008 technique mappings, Windows event IDs, LAPS and tiered admin controls, the flat-network, backup-server and cloud IAM gotchas, and the Microsoft Learn and MITRE sources, which are unreadable hosts.
Method: docs-checked 2026-11-09 against the Lockheed Martin Threat-Driven Approach white paper PDF
