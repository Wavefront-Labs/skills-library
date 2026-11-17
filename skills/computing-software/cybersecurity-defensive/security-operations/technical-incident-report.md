---
id: computing-software.cybersecurity-defensive.security-operations.technical-incident-report
name: technical-incident-report
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [technical-incident-report, incident-reporting, incident-response, post-incident-review, root-cause-analysis, report-writing]
level: practitioner
status: draft
description: "Write a technical incident report: timeline, initial access and attack path, affected systems, evidence, containment/eradication actions, root cause and recommendations."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.ncsc.gov.uk/collection/incident-management", "https://www.first.org/standards/frameworks/csirts/csirt_services_framework_v2.1"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Technical incident report

Audience: security, IT and engineering teams who must fix things and auditors who will check.

## Structure
1. **Summary**: incident ID, dates (detected, contained, closed), severity, category, short narrative.
2. **Detection**: how it was detected (alert, user report, third party), detection delay
   (first malicious activity to detection).
3. **Timeline** (UTC): attacker actions and responder actions in separate columns or tagged, each
   with source evidence reference.
4. **Attack path**: initial access, execution, persistence, privilege escalation, lateral movement,
   objectives; diagram plus ATT&CK mapping.
5. **Scope**: affected accounts, hosts, applications, data (with confidence); what was ruled out and how.
6. **Containment, eradication, recovery**: actions, timestamps, owners, validation evidence.
7. **Root cause and contributing factors**: technical (unpatched CVE, missing MFA) and process
   (alert not triaged, no asset owner). Use 5 whys / causal factor analysis.
8. **Indicators**: IOC appendix (defanged).
9. **Recommendations**: specific, owned, dated; categorised as prevent/detect/respond; link to tickets.
10. **Evidence register**: artefacts collected, storage location, hashes.

## Practice
- Draft the timeline during the incident; finalise within 2 weeks of closure.
- Review with responders and system owners for accuracy before circulation.
- Blameless tone: describe conditions and decisions, not individuals' failings.

## Gotchas
- Distinguish confirmed facts from assessments; label confidence.
- Legal privilege: if counsel directs, follow their distribution and labelling instructions.

## Verify
Each recommendation has an owner and ticket; timeline entries all cite evidence; detection gaps
identified have corresponding detection backlog items.
