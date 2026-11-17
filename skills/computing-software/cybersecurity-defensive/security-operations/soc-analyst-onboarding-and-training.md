---
id: computing-software.cybersecurity-defensive.security-operations.soc-analyst-onboarding-and-training
name: soc-analyst-onboarding-and-training
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-analyst-training, soc-management, onboarding, training-plan, cyber-range, analyst-development]
level: practitioner
status: draft
description: "Onboard and train SOC analysts: 30/60/90 day plan, shadowing, lab exercises, runbook sign-offs, qualification checklists per tier and continuous skills development."
sources: ["https://niccs.cisa.gov/workforce-development/nice-framework", "https://www.ncsc.gov.uk/collection/building-a-security-operations-centre", "https://www.sans.org/cyber-ranges/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SOC analyst onboarding and training

## 30/60/90 plan (tier 1)
- **Days 1-30**: accounts and tooling access; environment overview (network, critical assets,
  business); read core runbooks; shadow shifts; complete lab exercises on the SIEM and EDR; handle
  low-severity alerts with a buddy reviewing every disposition.
- **Days 31-60**: handle alert queue independently for signed-off alert types; mandatory review of
  all escalations; phishing and malware triage qualification.
- **Days 61-90**: full tier-1 qualification; join incident bridges as scribe; first runbook
  improvement contribution.

## Qualification checklist (per alert type)
Explain detection logic, perform triage steps, know escalation criteria, document correctly; signed
by a senior analyst after observing 5 cases.

## Training methods
- Lab with replayed real incidents (sanitised) and attack range data.
- Capture-the-flag/defensive ranges (Boss of the SOC, CyberDefenders, Blue Team Labs).
- Weekly case reviews: present an interesting case, what went well, what was missed.
- Purple-team participation to see attacks producing telemetry.
- Map skills to the NICE Framework work roles (e.g. Defensive Cybersecurity) for career paths.

## Continuous development
- Individual development plans with certifications aligned to role (e.g. GCIH, BTL1, CySA+).
- Rotation into detection engineering, CTI or IR for tier 2 growth.
- Protected learning time (e.g. 10% of shifts).

## Gotchas
- Throwing new analysts at the full queue on day one teaches bad habits and burns them out.
- Training that isn't environment-specific misses the most common error: not knowing what normal
  looks like here.

## Verify
Time-to-qualification, early-tenure quality review scores, and retention after 12 months tracked per cohort.
