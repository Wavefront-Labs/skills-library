---
id: computing-software.it-governance-risk-compliance.compliance-regulations-grc.pci-req-10-11-12-monitoring-policy
name: pci-req-10-11-12-monitoring-policy
category: computing-software
field: it-governance-risk-compliance
product: compliance-regulations-grc
tags:
- compliance-regulations-grc
- pci-req-10-11-12-monitoring-policy
level: practitioner
status: draft
description: Implement PCI DSS Requirements 10 (log and monitor), 11 (test security regularly) and 12 (policies, risk assessment, awareness, incident response, TPSP management).
sources:
- https://www.pcisecuritystandards.org/
- https://gdpr-info.eu/
- https://csrc.nist.gov/projects/olir
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Req 10-12 logging, testing and policy
**Goal:** monitoring and governance evidence.
- Req 10: audit logs for all components, daily automated review (v4), time sync, retain 12 months with 3 months immediately available.
- Req 11: quarterly internal and external vulnerability scans (external by ASV), penetration tests annually and after major change, change detection, intrusion detection.
- Req 12: security policy reviewed annually, targeted risk analyses (v4), security awareness, incident response plan tested, third-party service provider (TPSP) management with responsibility matrix.

## Self-check
Pull 12 months of logs and verify the oldest 9 months are retrievable.
