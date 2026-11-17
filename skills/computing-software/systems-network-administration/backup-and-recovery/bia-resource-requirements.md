---
id: computing-software.systems-network-administration.backup-and-recovery.bia-resource-requirements
name: bia-resource-requirements
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [resource-requirements, business-impact-analysis, bia, nist-800-34, recovery-resources, dependencies]
level: practitioner
status: docs-checked
description: "Identify the resources a process needs to recover in a NIST SP 800-34r1 BIA: facilities, personnel, equipment, software, data, vital records, and priorities."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIA steps 2 and 3: resource requirements and recovery priorities

**Goal:** list what is needed to resume each process as quickly as possible, then rank the system resources for recovery.

## Step 2: identify resource requirements (SP 800-34r1 section 3.2.2)
Realistic recovery needs a thorough evaluation of the resources required to resume mission/business processes and their interdependencies as quickly as possible. NIST's examples: facilities, personnel, equipment, software, data files, system components and vital records.

1. Work with management and the internal and external POCs associated with the system, so the complete set of system resources is identified.
2. Capture them in a simple table. NIST's Table 3-1 has columns: system resource/component, platform/OS/version (as applicable) and description (for example, the main application server).
3. Link each resource to the process it supports and to its RTO.

## Step 3: recovery priorities (section 3.2.3)
Priorities are the last BIA step. Take into account process criticality, outage impacts, tolerable downtime and system resources. The result is a system recovery priority hierarchy, which sets the sequence of recovery activities and resources. Then consider recovery measures and technologies that meet those priorities.

## Cost balance
Shorter RTOs cost more to implement (zero-downtime solutions and alternate processing sites), while a low-impact system with a longer RTO can use a simple tape backup. Weigh the cost of disruption against the cost of recovery; the balance point differs per organisation and system.

## Gotchas
Preventive controls found during the BIA (for example UPS, generators, fire suppression) may reduce or remove outage impacts and are preferred over recovery where feasible and cost-effective.

## Verify
A resource table exists per system, each resource maps to a process and RTO, and a recovery priority order is documented.

## Checked

2026-11-09. Read NIST SP 800-34 Rev. 1 sections 3.2 to 3.3 and Figure 3-3. Removed: ready.gov source (403, not read), the seven-category table with hardware, vendor and facility prompts, minimum-capacity sizing, recovery order (identity, network, databases), lead-time versus RTO check, hardware-bound licences, sole-knowledge staff and SaaS notes (none stated). Draft called this step 3; SP 800-34 numbers it step 2.

Method: documentation only; no commands were run.
