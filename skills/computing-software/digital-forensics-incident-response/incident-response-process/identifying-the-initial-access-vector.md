---
id: computing-software.digital-forensics-incident-response.incident-response-process.identifying-the-initial-access-vector
name: identifying-the-initial-access-vector
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [initial-access-vector, initial-access, root-cause-analysis, mitre-attack, patient-zero, dfir]
level: advanced
status: draft
description: "Identify the initial access vector and patient zero: working backwards from earliest evidence through phishing, exposed services, valid accounts and supply chain."
sources: ["https://attack.mitre.org/tactics/TA0001/", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Identifying the initial access vector

**Goal:** prove how the attacker first got in, so eradication closes the right door and the
report answers the question regulators and insurers always ask.

## Work backwards
1. Take the **earliest confirmed malicious event** (first malicious process, first bad logon).
2. Ask what made it possible and pivot one step earlier, repeatedly, until you reach an
   external entry point. Keep each hop backed by evidence.
3. Keep a hypothesis list and eliminate rather than pick the first plausible story.

## Common vectors (MITRE ATT&CK TA0001) and their evidence
| Vector | Look at |
|---|---|
| Phishing attachment/link (T1566) | Mail logs/message trace, Outlook OST attachments, browser downloads, Zone.Identifier ADS, Office child processes, LNK/ISO mounts |
| Exploited public-facing app (T1190) | Web/WAF logs around first activity, new files under web roots, process children of w3wp/java/httpd, version vs CISA KEV catalog |
| External remote services (T1133) | VPN, Citrix, RDP gateway logs: new device, unusual geo, brute force then success |
| Valid accounts (T1078) | IdP sign-ins, infostealer exposure of the user, MFA fatigue patterns, password spray |
| Drive-by / malvertising (T1189) | Proxy/DNS logs, browser history, fake installer downloads (SEO poisoning) |
| Supply chain / trusted relationship (T1195, T1199) | Updates of third-party software, MSP RMM tools (ScreenConnect, AnyDesk) sessions |
| Removable media (T1091) | USB artefacts, autorun, LNK on removable drives |

## Gotchas
- Log retention shorter than dwell time: say "most likely" with the reasoning, not certainty.
- Edge devices (VPN appliances, firewalls) rarely have forensic logs; collect their logs and
  config early, and check vendor advisories and integrity-check tools.
- The first host you found is rarely patient zero.

## Verify
State the vector with confidence level and the evidence chain. A peer should be able to
follow every hop from the external entry to the earliest malicious event.
