---
id: computing-software.cybersecurity-defensive.security-architecture.data-loss-prevention
name: data-loss-prevention
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [data-protection, data-loss-prevention, dlp, endpoint-dlp, email-dlp, cloud-dlp, casb, sensitive-information-types, exact-data-match, policy-tuning]
level: practitioner
status: draft
description: "Deploy DLP across email, endpoint and cloud apps: start in audit mode, use precise detections (EDM, fingerprints, labels), tune false positives, then enforce."
sources: ["CompTIA Security+ SY0-701 objective 4.5 (DLP)", "CIS Control 3.13 (deploy a DLP solution)", "Microsoft Learn - Microsoft Purview Data Loss Prevention"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data loss prevention

**Goal:** stop or flag sensitive data leaving approved locations, with few enough false
positives that users and analysts do not ignore it.

## Channels
| Channel | Controls |
|---|---|
| Email | Transport rules / DLP: block or encrypt external mail with sensitive content |
| Endpoint | Block copy to USB, upload to unapproved sites, print, paste into web apps |
| Cloud apps / SaaS | Sharing links, external sharing, CASB inline or API |
| Network / web | SWG inspecting uploads (needs TLS inspection) |
| Generative AI tools | Block or warn on pasting sensitive data into unsanctioned AI sites |

## Detection methods (most to least precise)
1. **Labels** applied by users or auto-labelling.
2. **Exact Data Match (EDM)**: hashed copy of your actual customer table; matches real records only.
3. **Document fingerprinting**: forms and templates (e.g. HR forms).
4. **Sensitive information types**: pattern + checksum + keywords (card numbers with Luhn check near "card").
5. **Trainable classifiers / ML**: source code, contracts; useful but noisy.
Regex alone generates a flood: always add confidence, proximity keywords and instance counts (e.g. 10+ card numbers).

## Rollout
1. Audit/simulation mode for 2-4 weeks; review matches by rule.
2. Tune: exclusions for business processes (payroll to the bank), raise thresholds.
3. Policy tips (warn with justification override) before blocking; users learn the rule.
4. Block for the highest-risk channels and data first (Restricted data to personal email/USB).
5. Route incidents to a triage queue with data owner involvement, not only security.

## Gotchas
- DLP does not stop a determined insider (photos of screens, encryption); it stops accidents and casual exfiltration.
- Endpoint DLP on unmanaged devices does not exist; combine with conditional access to block downloads there.
- Incident data contains the sensitive data itself: restrict who can view DLP evidence.

## Verify
- [ ] Test files (synthetic card numbers, EDM test records) are detected on each channel.
- [ ] False-positive rate per rule tracked and under the agreed threshold before enforcement.
