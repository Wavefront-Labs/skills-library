---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cspm
name: cspm
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-security-architecture, cspm, cloud-security-posture-management, cnapp, security-hub, defender-for-cloud, security-command-center, prowler, misconfiguration-detection, finding-triage]
level: practitioner
status: draft
description: "Run cloud security posture management: enable native CSPM org-wide, pick standards, route and triage findings by severity and owner, suppress with reasons."
sources: ["https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html", "https://learn.microsoft.com/azure/defender-for-cloud/concept-cloud-security-posture-management", "https://cloud.google.com/security-command-center/docs/security-command-center-overview", "https://github.com/prowler-cloud/prowler"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud security posture management

## Steps
1. **Enable org-wide** with a delegated admin in the security tooling account:
   AWS Security Hub (+ AWS Config recorder in all regions/accounts), Microsoft Defender for Cloud
   (foundational CSPM free; Defender CSPM plan adds attack paths), Google Security Command Center
   (Standard/Premium/Enterprise). Multi-cloud: a CNAPP (Wiz, Prisma Cloud, Orca) or open-source Prowler.
2. **Standards**: CIS benchmarks + provider foundational best practices; add PCI/NIST packs where in scope.
3. **Route findings** to owners via account/subscription ownership metadata — EventBridge /
   Logic Apps / Pub/Sub to ticketing, not one shared inbox.
4. **Triage policy**: critical (public data exposure, admin keys) — hours; high — days;
   medium/low — backlog with SLA. Prioritise by exposure (internet-reachable + sensitive data + exploitable).
5. **Suppress deliberately** with reason and expiry (e.g. a public website bucket), never bulk-mute.
6. **Prevent recurrence**: turn frequent findings into preventive policies and IaC module defaults.
7. Track posture score and open criticals by team over time.

## Gotchas
- Config recording costs money at scale (AWS Config per configuration item) — scope recording thoughtfully, but don't leave regions dark.
- Duplicate findings from multiple tools; pick one source of truth for tickets.

## Verify
- [ ] All accounts/subscriptions/projects report to CSPM, including new ones automatically.
- [ ] Mean time to remediate criticals tracked and within SLA.
