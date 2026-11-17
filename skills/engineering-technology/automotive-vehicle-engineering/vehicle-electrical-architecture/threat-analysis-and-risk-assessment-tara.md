---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.threat-analysis-and-risk-assessment-tara
name: threat-analysis-and-risk-assessment-tara
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [tara, iso-21434, threat-analysis, attack-feasibility, damage-scenario, cybersecurity-goal, risk-treatment]
level: practitioner
status: gated
description: "Run a TARA under ISO/SAE 21434: assets, damage and threat scenarios, impact and feasibility rating, risk value, treatment decisions and goals."
sources:
  - "ISO/SAE 21434:2021 Road vehicles - Cybersecurity engineering (https://www.iso.org/standard/70918.html)"
  - "UN Regulation No 155 as published in the EU Official Journal, Annex 5 threat list (https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:42021X0387)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Threat analysis and risk assessment (TARA)

Professional practice guidance; follow ISO/SAE 21434 and your cybersecurity team's process. Regulatory compliance (UN R155) is decided with your approval authority.

1. **Asset identification:** functions, data and components that need protection and their cybersecurity properties (confidentiality, integrity, availability); from the item definition and architecture.
2. **Damage scenarios:** consequences of loss of a property; rate impact in four categories: safety, financial, operational, privacy (SFOP) with levels negligible to severe (gated: unconfirmed, source is paywalled or blocked).
3. **Threat scenarios:** how a property could be compromised, often using STRIDE (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege).
4. **Attack path analysis:** steps an attacker takes; interfaces (OBD, wireless, cellular, USB, supply chain).
5. **Attack feasibility rating:** by attack potential (elapsed time, expertise, knowledge, window of opportunity, equipment), CVSS-based, or attack-vector-based method; levels very low to high (gated: unconfirmed, source is paywalled or blocked).
6. **Risk value:** combine impact and feasibility using the organisation's matrix (the standard gives an example 1-5 scale (gated: unconfirmed, source is paywalled or blocked)).
7. **Risk treatment:** avoid, reduce (controls), share (insurance, contract), retain (accept with rationale); define cybersecurity goals and later claims.
8. Link to the cybersecurity concept and requirements; repeat when architecture or threat landscape changes.

**Gotchas:** treating TARA as a one-time paper exercise; no link to testing.

## Verify
- [ ] Every asset has damage scenarios with SFOP impact and rationale.
- [ ] Each risk above the acceptance level has a treatment decision with requirements.
