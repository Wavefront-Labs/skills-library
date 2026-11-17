---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.threat-detection
name: threat-detection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, detection-and-response, threat-detection, guardduty, defender-for-cloud, security-command-center, siem, microsoft-sentinel, detection-engineering, cloud-detections]
level: practitioner
status: draft
description: "Set up cloud threat detection: enable native detectors org-wide, centralise findings and logs into a SIEM, write cloud-specific detections, and route alerts with context."
sources: ["https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html", "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-cloud-introduction", "https://cloud.google.com/security-command-center/docs/concepts-event-threat-detection-overview", "https://attack.mitre.org/matrices/enterprise/cloud/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threat detection and SIEM integration

## Steps
1. **Native detectors in every account/region**, delegated admin in the security account:
   GuardDuty (+ S3, EKS, runtime, Lambda, RDS protection plans as needed), Microsoft Defender for
   Cloud plans, Security Command Center Event Threat Detection.
2. **Central log sources**: control-plane audit logs (CloudTrail org trail, Azure Activity Log +
   Entra ID sign-in/audit logs, Cloud Audit Logs), DNS logs, VPC flow logs, WAF logs, k8s audit
   logs, IdP logs.
3. **SIEM**: Microsoft Sentinel, Splunk, Chronicle/Google SecOps, Elastic — ingest findings
   (Security Hub/EventBridge, Defender connectors) and raw logs needed for investigation.
4. **Cloud-specific detections** (map to MITRE ATT&CK Cloud): root/break-glass login, MFA
   disabled, new access keys for privileged users, `StopLogging`/`DeleteTrail`, security tool
   disabled, public exposure changes, unusual `AssumeRole` chains, cross-account trust added,
   crypto-mining instance types/regions, mass `GetObject` from new IPs.
5. **Alert routing** with context: account owner, resource, actor, recent changes; severity → on-call vs queue.
6. Tune false positives with suppression rules tied to reasons; test detections (Stratus Red Team, Atomic Red Team cloud tests).

## Verify
- [ ] Every account/region reports to detectors (no dark regions — attackers like unused ones).
- [ ] Simulated `StopLogging` produces an alert within minutes.
