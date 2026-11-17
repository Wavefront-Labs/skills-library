---
id: computing-software.cybersecurity-defensive.security-operations.mdr-mssp-provider-management
name: mdr-mssp-provider-management
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [mdr-provider-management, mssp, soc-management, vendor-management, sla, managed-detection-and-response]
level: advanced
status: draft
description: "Manage an MDR or MSSP provider: scope and RACI, onboarding log sources, SLAs and service credits, escalation paths, performance reviews and exit planning."
sources: ["https://www.ncsc.gov.uk/collection/building-a-security-operations-centre", "https://www.cisa.gov/resources-tools/resources/cyber-essentials", "https://www.gartner.com/en/documents/market-guide-for-managed-detection-and-response-services"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# MDR and MSSP provider management

## Contract and scope
- What they monitor (log sources, EDR, cloud, identity), hours (24x7), what they do on detection:
  notify only, guided response, or active response (isolate host, disable user) with pre-authorised
  playbooks.
- RACI per activity: detection content, tuning, triage, containment, forensics, reporting,
  threat hunting, log source health.
- SLAs: time to notify by severity (e.g. critical 15-30 min), time to respond, log source outage
  notification, monthly reporting. Service credits for breaches.
- Data: where logs are stored, retention, access to raw data, ownership, return/deletion at exit.

## Onboarding
- Asset and identity context (critical assets, VIPs, admin accounts), network diagrams, change
  calendars, allowlists of known activity, escalation contact tree with phone numbers.
- Agree severity definitions mapped to your incident classification.
- Test escalation paths end-to-end (fake critical at 3 am).

## Ongoing governance
- Monthly service review: alert volumes, true-positive rates, SLA attainment, detections added,
  tuning requests status, log source health, notable incidents.
- Quarterly: purple-team or simulation exercise to validate detection and response; measure the
  provider's time to detect.
- Track tickets they escalate that were noise (quality) and incidents you found that they missed.

## Exit planning
Keep detection logic visible (or owned), ensure raw logs are in your tenancy (e.g. your SIEM/
data lake), document integrations, and maintain internal capability to run triage briefly during
transition.

## Gotchas
- "We monitor everything" without per-source detection coverage evidence; ask for ATT&CK coverage
  mapped to your data.
- Active response without clear authorisation creates outages; define exclusion lists.

## Verify
Annual scorecard: SLA attainment, simulation results, coverage map, and incident quality; renewal
decisions reference it.
