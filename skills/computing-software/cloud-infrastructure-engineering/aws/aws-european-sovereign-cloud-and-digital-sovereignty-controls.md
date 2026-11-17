---
id: computing-software.cloud-infrastructure-engineering.aws.aws-european-sovereign-cloud-and-digital-sovereignty-controls
name: aws-european-sovereign-cloud-and-digital-sovereignty-controls
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, shared-responsibility, sovereign-cloud, european-sovereign-cloud, digital-sovereignty, data-residency, external-key-store]
level: practitioner
status: draft
description: "Digital sovereignty on AWS: the AWS European Sovereign Cloud model, data residency guardrails, external key stores, Nitro isolation and dedicated infrastructure options."
sources: ["AWS - AWS European Sovereign Cloud overview", "AWS Digital Sovereignty Pledge", "AWS Control Tower User Guide - Data residency controls", "AWS KMS Developer Guide - External key stores (XKS)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AWS European Sovereign Cloud and digital sovereignty controls

## Sovereignty dimensions
| Dimension | Question | AWS levers |
|---|---|---|
| Data residency | where is data stored and processed? | region choice, SCP/Control Tower data residency controls, service-specific residency features |
| Operator access | who can access systems and data? | Nitro System (no operator access to customer memory), access controls, sovereign-operated regions |
| Encryption and keys | who controls keys? | KMS customer managed keys, CloudHSM, **external key store** (keys in your HSM outside AWS) |
| Resilience and independence | can it run under geopolitical stress? | separate partitions, local operations, multi-region within jurisdiction |
| Transparency | evidence | AWS Artifact reports, Nitro third-party assessments |

## AWS European Sovereign Cloud
- An independent cloud for Europe, physically and logically separate from existing AWS Regions,
  with infrastructure located in the EU and operated and supported by EU-resident personnel; the
  first region is in Brandenburg, Germany. It has its own account and identity foundations, billing and metadata kept in the EU.
- Check current status, service list and how accounts are created before planning; it does not share accounts, IAM or resources with commercial regions, so cross-partition integrations need explicit design.

## Controls in commercial regions
```json
{"Effect":"Deny","NotAction":["iam:*","organizations:*","sts:*","support:*","cloudfront:*","route53:*"],
 "Resource":"*","Condition":{"StringNotEquals":{"aws:RequestedRegion":["eu-central-1","eu-west-1"]}}}
```
- SCP (or Control Tower region deny and data residency controls) restricts use to approved regions; global services need exceptions.
- KMS external key store (XKS): AWS calls your external key manager for every cryptographic operation; you can cut off access. Adds latency and availability dependency on your HSM.
- Dedicated Local Zones and Outposts for location-specific or on-premises processing.
- Logging and backups also in-region (CloudTrail, Backup copy destinations within jurisdiction).

## Assessment checklist
- [ ] Data classification identifies sovereign data and its allowed locations.
- [ ] Region guardrails enforced via SCP with tested exceptions.
- [ ] Key control model chosen (CMK, CloudHSM, XKS) and documented with availability impact.
- [ ] Support and operational access model reviewed (including third parties and AWS support cases containing data).

## Gotchas
- Some features rely on global services or cross-region processing (e.g. certain ML or edge services); verify each one.
- Cross-partition data flows (sovereign cloud to commercial) re-introduce residency questions.

## Verify
- [ ] Attempted resource creation in a non-approved region is denied.
- [ ] Sovereignty requirements mapped to controls with evidence for auditors.
