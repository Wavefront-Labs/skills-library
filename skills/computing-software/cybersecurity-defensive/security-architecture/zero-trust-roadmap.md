---
id: computing-software.cybersecurity-defensive.security-architecture.zero-trust-roadmap
name: zero-trust-roadmap
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [zero-trust-roadmap, zero-trust, cisa-zero-trust-maturity-model, nist-sp-800-207, zero-trust-migration, maturity-assessment]
level: advanced
status: draft
description: "Plan a multi-year zero trust migration: baseline against the CISA maturity model, pick protect surfaces, sequence identity-device-network-app pillars and measure progress."
sources: ["https://www.cisa.gov/zero-trust-maturity-model", "https://csrc.nist.gov/pubs/sp/800/207/final", "https://www.nccoe.nist.gov/projects/implementing-zero-trust-architecture"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zero trust migration roadmap

**Goal:** turn "we are doing zero trust" into a sequenced, funded, measurable plan.

## 1. Baseline
Score each CISA ZTMM v2 pillar (Identity, Devices, Networks, Applications and Workloads, Data) plus the
cross-cutting capabilities (Visibility and Analytics, Automation and Orchestration, Governance) as
Traditional / Initial / Advanced / Optimal. Evidence, not opinion: export the MFA coverage report, the
device compliance percentage, the count of flat VLANs, the list of apps still on VPN-only access.

## 2. Pick protect surfaces (NIST SP 800-207 / Kindervag five-step)
1. Identify the protect surface (crown-jewel data, apps, assets, services - DAAS).
2. Map transaction flows to and from it.
3. Architect the micro-perimeter (policy enforcement point in front of it).
4. Write policy (who, what device, when, where, why).
5. Monitor and maintain.
Start with one protect surface that is valuable and politically achievable (e.g. finance ERP admin access),
not the whole estate.

## 3. Sequence (typical order, because each depends on the previous)
| Phase | Delivers | Dependency |
|---|---|---|
| Identity | Single IdP, phishing-resistant MFA for admins, conditional access | Nothing |
| Device | Inventory, MDM/EDR, compliance signal into the IdP | Identity (policy engine) |
| Access | ZTNA/identity-aware proxy replaces VPN per app | Identity + device signal |
| Network | Microsegmentation of the protect surface, deny-by-default east-west | Flow mapping |
| Data | Classification labels feeding DLP and access policy | Above signals |
| Analytics | Continuous evaluation, risk-based session revocation | Logs from all pillars |

## 4. Measure
Track per quarter: % of apps behind the policy engine, % of users on phishing-resistant MFA, % of devices
reporting compliance, number of standing admin accounts, VPN concurrent users (should fall).

## Gotchas
- Buying a ZTNA product is not a roadmap; without identity and device signals it is just a new VPN.
- Legacy apps (Kerberos/NTLM, thick clients) stall programmes - plan them explicitly
  (see `computing-software.cybersecurity-defensive.security-architecture.legacy-app-zero-trust`).
- Keep the VPN as fallback until the ZTNA path has carried production traffic for a full business cycle.

## Verify
- [ ] Maturity baseline scored with evidence per pillar.
- [ ] First protect surface live with policy decisions logged.
- [ ] Quarterly metrics trending in the right direction.
