---
id: computing-software.cybersecurity-defensive.cloud-security.cryptomining-response
name: cryptomining-response
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cryptomining-response, cryptojacking, guardduty-cryptocurrency, compromised-credentials, cost-anomaly-detection, cloud-incident-response]
level: practitioner
status: docs-checked
description: "Respond to cloud cryptomining compromises: detection signals, finding the entry point (leaked keys, exposed services, poisoned images), containment and cleanup across regions."
sources: ["https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-ec2.html", "https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html", "https://cloud.google.com/security-command-center/docs/cryptomining-detection-best-practices", "https://attack.mitre.org/techniques/T1496/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cryptomining compromise response

Cryptomining (ATT&CK T1496 Resource Hijacking) is the most common outcome of leaked cloud credentials
and exposed services. It is noisy - and often a sign of a broader compromise.

## Detection signals
- GuardDuty `CryptoCurrency:EC2/BitcoinTool.B!DNS`, `Impact:EC2/BitcoinDomainRequest.Reputation`, Runtime Monitoring mining findings; the equivalent cryptomining detections in Security Command Center and Defender for Cloud (see each product's findings list).
- Cost anomaly detection / budgets: sudden GPU or large instance spend, new regions.
- Quota increase requests, new instances in regions you never use, Kubernetes pods with high CPU and mining pool connections.

## Entry points to check
1. Leaked access keys (public repos, CI logs) -> CloudTrail `RunInstances`, `CreateUser`, `CreateAccessKey`, `CreateLoginProfile` from unusual IPs/user agents.
2. Exposed services: Kubernetes API/dashboard, Docker API, Jupyter, Redis, vulnerable web apps.
3. Poisoned container images from public registries.
4. Compromised CI/CD (GitHub Actions secrets).

## Contain and clean
- Disable the abused credentials; quarantine IAM user with a deny-all policy; revoke role sessions.
- Inventory **all regions** for instances, spot requests, launch templates, auto scaling groups, Lambda, ECS/EKS workloads, SageMaker notebooks created during the window (CloudTrail by principal) - attackers create persistence (new IAM users, roles, access keys, Lambda backdoors) beyond the miners.
- Snapshot one miner instance for forensics, then terminate.
- Remove persistence; rotate secrets the attacker could read.
- SCP to deny regions not in use and expensive instance families where unused.

## Billing
Open a support case with the provider about the unauthorised usage; any concession is the provider's decision.

## Checked

2026-10-28: confirmed on the GuardDuty EC2 finding types page: CryptoCurrency:EC2/BitcoinTool.B!DNS and Impact:EC2/BitcoinDomainRequest.Reputation exist. Removed: mining pool port list, Docker API port, named SCC and Defender alert titles, and the billing-concession claim (not confirmed in the pages read). ATT&CK T1496 and the other CloudTrail event names were not re-checked this batch.

Method: documentation only; no commands were run.

## Verify
- [ ] No resources created by the attacker remain in any region (Resource Explorer/Config aggregator query by creation time).
- [ ] Root cause fixed (key removed from repo and rotated, service no longer exposed).
