---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.security-log-coverage
name: security-log-coverage
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, detection-and-response, security-log-coverage, audit-logging, log-sources, mitre-attack]
level: practitioner
status: draft
description: "Ensure security log source coverage: required cloud logs per provider, org-wide enablement, data events, retention, gap analysis against ATT&CK and health checks."
sources: ["https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html", "https://learn.microsoft.com/azure/azure-monitor/essentials/activity-log", "https://cloud.google.com/logging/docs/audit", "https://attack.mitre.org/matrices/enterprise/cloud/", "https://www.cisa.gov/resources-tools/resources/best-practices-event-logging-and-threat-detection"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security log source coverage

## Steps
1. **Baseline sources per provider**:
   - AWS: organisation CloudTrail (management events, plus S3/Lambda data events for
     sensitive buckets), VPC Flow Logs, Route 53 Resolver query logs, ELB/CloudFront/WAF logs,
     GuardDuty, Config.
   - Azure: Activity Log, Entra ID sign-in and audit logs, resource diagnostic logs (Key Vault,
     Storage, SQL), NSG/VNet flow logs, Defender alerts.
   - Google: Admin Activity (always on), Data Access audit logs (off by default for most
     services; enable for sensitive ones), VPC Flow Logs, Cloud DNS logs, Workspace logs.
   - Plus IdP, Kubernetes audit logs, SaaS audit logs, EDR.
2. **Enforce org-wide**: org trails, Azure Policy diagnostic settings, org-level log sinks.
3. **Map to ATT&CK cloud techniques**: for each priority technique, which source and
   detection covers it; gaps become backlog.
4. **Retention**: hot searchable 90 days+, archive 1 year+ (regulatory may require more);
   immutable storage in a log archive account.
5. **Health monitoring**: alert when a source stops sending (volume drops to zero, trail
   stopped, diagnostic setting deleted).

## Gotchas
- Google Data Access logs and AWS data events are off by default; most exfiltration hides there.
- Logging everything at full verbosity into the SIEM is unaffordable; tier destinations.

## Verify
- [ ] Coverage matrix: source to accounts enabled, percent coverage.
- [ ] Silent-source alerting tested.
