---
id: computing-software.systems-network-administration.backup-and-recovery.fips-199-impact-levels-for-contingency-planning
name: fips-199-impact-levels-for-contingency-planning
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [fips-199, security-categorization, iscp-templates, nist-800-34, business-impact-analysis, contingency-plan]
level: practitioner
status: docs-checked
description: "Use the FIPS 199 availability impact level to pick the SP 800-34 ISCP template, recovery strategy, alternate site need and test type."
sources:
  - https://csrc.nist.gov/pubs/fips/199/final
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FIPS 199 impact levels drive the contingency plan

**Goal:** right-size contingency measures by the system's security category, not by gut feel.

## Categorise (FIPS 199)
The security category of a system is SC = {(confidentiality, impact), (integrity, impact), (availability, impact)}, each value LOW, MODERATE or HIGH. For a system, each objective takes the highest value (high-water mark) among the information types on it. NOT APPLICABLE cannot be used for a system's objectives. SP 800-34 Rev. 1 says contingency planning considerations and strategies address the impact level of the **availability** objective, and that the availability category is the basis of the BIA.

## What SP 800-34 Rev. 1 ties to each level
| Availability level | Example target priority (Table 3-2) | Example backup / strategy (Table 3-2) | Alternate site | Test type (section 3.5.4) |
|---|---|---|---|---|
| Low | Low priority | Tape backup; relocate or cold site | Not required (CP-6, CP-7); organisation may choose to | Tabletop at an organisation-defined frequency |
| Moderate | Important or moderate priority | Optical backup, WAN/VLAN replication; cold or warm site | Plan should include a strategy to operate at an alternate facility for an extended period | Functional exercise, including recovering from backup media |
| High | Mission-critical or high priority | Mirrored systems and disc replication; hot site | Same as moderate; high-availability options (redundant load-balanced systems at alternate sites, data mirroring, offsite database replication) only for high-availability systems | Full-scale functional exercise including failover to the alternate location and full recovery and reconstitution |

Table 3-2 is described by the guide as an example. The guide also says a moderate-availability system requires only the first system backup control enhancement (CP-9 [1]) and that plans for moderate or high systems should be reviewed more often.

## Steps
1. Get the system's FIPS 199 categorisation from the security plan; if none exists, do it with the system owner.
2. Pick the matching ISCP template from SP 800-34 Appendix A (there are three, for low, moderate and high) and keep its structure.
3. Pull the CP family controls for your baseline from SP 800-53 and record how each is met (practice).
4. Compare RTO/RPO from the BIA with the strategy: a high-availability system with weekly tape and no alternate site does not match the guide's example table (practice).

## Gotchas (practice)
- Categorisation is per system; a low system hosted on shared high-impact infrastructure still inherits shared outages.
- Availability high with confidentiality low is common (public websites); do not lower the contingency effort because the data is public.

## Verify
Security plan, BIA and ISCP state the same impact level, and each CP control applicable to that baseline has an implementation statement.

## Checked

2026-11-09. Checked against FIPS 199 (full PDF, 13 pages: system categorisation, high-water mark, not-applicable rule) and NIST SP 800-34 Rev. 1 (PDF behind the csrc.nist.gov page), sections 2.1, 3.1, 3.4.1, 3.4.3, 3.5.4 and 3.6. Targeted reads of 800-34, not the whole 149 pages. Removed: the SP 800-53 source (not read), the specific CP-9 and CP-4 enhancement lists, "geographic separation" and "priority telecom" requirements, "yearly" test frequencies, "offsite optional" for low, and the "SP 800-34 Table 3-x" label. The table now follows Table 3-2 and section 3.5.4. Steps 3-4 and the gotchas are practice.

Method: documentation only; no commands were run.
