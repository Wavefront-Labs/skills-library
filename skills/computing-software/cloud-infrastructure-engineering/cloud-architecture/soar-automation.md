---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.soar-automation
name: soar-automation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, detection-and-response, soar, security-automation, playbooks, automated-response]
level: practitioner
status: draft
description: "Automate security response (SOAR): choose cases to automate, event-driven playbooks in native tooling, human approval gates, safe containment actions and metrics."
sources: ["https://learn.microsoft.com/azure/sentinel/automation/automation", "https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-cloudwatch-events.html", "https://cloud.google.com/chronicle/docs/soar/overview-and-introduction/soar-overview", "https://csrc.nist.gov/pubs/sp/800/61/r3/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated security response (SOAR)

## Steps
1. **Pick high-volume, low-ambiguity cases first**: enrichment (whois, asset owner, user
   context), public bucket remediation, disabling leaked access keys, isolating a compromised
   instance, phishing triage.
2. **Event-driven wiring**: findings (GuardDuty/Security Hub via EventBridge, Defender via
   Sentinel automation rules, SCC via Pub/Sub) trigger playbooks (Step Functions/Lambda,
   Logic Apps, Google SecOps SOAR playbooks).
3. **Tiered actions**: enrich and ticket automatically; reversible containment automatically
   for high-confidence detections (tag-based quarantine security group, revoke sessions);
   destructive or business-impacting actions behind a human approval step (chat button).
4. **Safety**: idempotent actions, allow-lists for critical resources, rate limits, full
   audit log of what automation did and why.
5. **Test** playbooks with simulated findings (GuardDuty sample findings, Defender sample
   alerts) in non-prod; version as code.
6. **Measure**: mean time to respond/contain, analyst hours saved, false-action rate.

## Gotchas
- Auto-isolating a production database on a false positive is an outage; gate it.
- Playbooks break silently when APIs change; schedule synthetic tests.

## Verify
- [ ] Each playbook tested with sample findings.
- [ ] MTTR before/after automation reported.
