---
id: computing-software.cybersecurity-defensive.security-operations.soc-cmm-maturity-assessment
name: soc-cmm-maturity-assessment
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-cmm, soc-management, maturity-assessment, capability-maturity-model, soc-roadmap]
level: advanced
status: draft
description: "Assess SOC maturity with SOC-CMM: domains (business, people, process, technology, services), scoring maturity and capability, setting targets and a roadmap."
sources: ["https://www.soc-cmm.com/", "https://www.soc-cmm.com/downloads/", "https://www.first.org/standards/frameworks/csirts/csirt_services_framework_v2.1"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SOC maturity assessment with SOC-CMM

SOC-CMM is a free self-assessment model (spreadsheet-based) scoring SOC **maturity** (0-5) across
five domains and **capability** (0-3) in technology and services.

## Domains
- **Business**: drivers, customers, charter, governance, privacy.
- **People**: employees, roles and hierarchy, people management, knowledge management, training.
- **Process**: SOC management, operations and facilities, reporting, use case management, detection
  engineering and validation.
- **Technology**: SIEM, IDPS, security analytics, automation and orchestration, EDR/NDR etc.
- **Services**: security monitoring, incident response, security analysis and forensics, threat
  intelligence, threat hunting, vulnerability management, log management.

## Running the assessment
1. Choose scope (which SOC services) and participants (lead, analysts, engineers, stakeholders).
2. Answer each question with evidence in mind; interview rather than self-report by one person.
3. Set **target** maturity per element based on business need (not everything must be 5).
4. Output: radar charts of current vs target, gap list.
5. Version (basic vs advanced); keep the same version for year-on-year comparison.

## From gaps to roadmap
- Prioritise gaps that affect detection/response outcomes (use case management, detection
  validation, IR process) over documentation-only gaps.
- Roadmap items with owners, quarters and measurable outcomes (e.g. "use case lifecycle with
  quarterly review: 100% production detections reviewed").
- Re-assess annually.

## Gotchas
- Self-assessment inflation: require evidence for scores of 3+.
- Maturity scores do not equal effectiveness; pair with purple-team results and metrics.

## Verify
Assessment file with evidence references, agreed targets signed off by SOC owner, and roadmap items
tracked to completion.
