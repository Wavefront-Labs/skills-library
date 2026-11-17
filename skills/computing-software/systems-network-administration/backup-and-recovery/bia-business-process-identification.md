---
id: computing-software.systems-network-administration.backup-and-recovery.bia-business-process-identification
name: bia-business-process-identification
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [business-process-identification, business-impact-analysis, bia, nist-800-34, mission-essential-functions, contingency-planning]
level: practitioner
status: docs-checked
description: "Identify the mission and business processes a system supports for a NIST SP 800-34r1 BIA: work with management and POCs, rate impact, set downtime."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIA step 1: determine business processes and recovery criticality

**Goal:** a validated list of the mission/business processes a system supports, with the impact of disruption and the tolerable downtime for each.

## Why
The BIA correlates the system with the critical mission/business processes and services it provides and, from that, characterises the consequences of a disruption. NIST says to perform it in the Initiation phase of the SDLC and to repeat it during Development/Acquisition if the design and components change.

## Method (SP 800-34r1 section 3.2.1)
1. A system often supports several processes with different views of how important its services are. The ISCP Coordinator works with management and internal and external points of contact (POCs) to identify and validate the processes that depend on or support the system.
2. Include as POCs the organisations that provide data to or receive data from the system, and the POCs of any interconnected systems, so the full range of support (security, managerial, technical, operational) is characterised.
3. Analyse each process's impacts in terms of availability, integrity, confidentiality and the system's FIPS 199 impact level. The FIPS 199 availability category is the basis of the BIA.
4. Add organisation-specific processes and impacts in units meaningful to the organisation, on a scale of severity if the process could not be performed (for example a "Costs" category in staffing, overtime or fee terms).
5. With process owners, leadership and business managers, determine the acceptable downtime if the process or its data were unavailable (see maximum-tolerable-downtime-bia). The downtime should reflect the maximum time the organisation can tolerate while still maintaining the mission.
6. Record process, potential impacts, MTD and the system components with their RTOs, as in the figure in section 3.2.

## Gotchas
- Systems that support COOP functions are identified in the process-based BIA; other systems use the system-based BIA.
- Do not let IT answer for business owners; NIST has process owners and business managers set the acceptable downtime.

## Verify
Each process has a named owner, an impact statement, an MTD and the supporting components, agreed with its owner.

## Checked

2026-11-09. Read NIST SP 800-34 Rev. 1 section 3.2 to 3.2.1 and footnotes. Removed: ISO source (not read), interview length and questionnaire, the process inventory table and payroll example, hidden-dependency list, seasonal and batch advice (none stated).

Method: documentation only; no commands were run.
