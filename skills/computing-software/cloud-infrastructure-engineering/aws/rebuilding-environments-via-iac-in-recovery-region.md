---
id: computing-software.cloud-infrastructure-engineering.aws.rebuilding-environments-via-iac-in-recovery-region
name: rebuilding-environments-via-iac-in-recovery-region
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, disaster-recovery, infrastructure-rebuild, iac-recovery, multi-region-iac, stacksets, pilot-light]
level: practitioner
status: gated
description: "Make infrastructure-as-code redeployable into a recovery region: region-agnostic templates, replicated artifacts (AMIs, images, keys, secrets), quotas, and timed rebuild drills."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getavailabilityzones.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rebuilding environments via IaC in the recovery region

**Goal:** for backup-and-restore or pilot-light DR, `deploy --region <dr>` recreates the
environment from code within the RTO, and the data restores into it.

## Make the code region-agnostic
- No hard-coded regions, AZ names, AMI ids, account ids or ARNs: use `AWS::Region`,
  `Fn::GetAZs`, SSM public parameters for AMIs, and mappings per region.
- Globally unique names (S3 buckets) include the region: `orders-${AWS::AccountId}-${AWS::Region}`.
- Avoid features missing in the DR region (check service and instance type availability).
- Terraform: provider alias per region and workspaces/var files; CDK: one Stage per region.

## Replicate artifacts continuously
| Artifact | Mechanism |
|---|---|
| AMIs | Image Builder distribution settings to the DR region; `copy-image` for others (gated: unconfirmed, source is paywalled or blocked) |
| Container images | ECR replication rules (gated: unconfirmed, source is paywalled or blocked) |
| Lambda code | deploy artifacts bucket replicated (S3 CRR) or rebuilt by pipeline |
| KMS keys | multi-Region keys (replica in DR region) so encrypted backups decrypt (gated: unconfirmed, source is paywalled or blocked) |
| Secrets | Secrets Manager replica secrets; Parameter Store copied by pipeline (gated: unconfirmed, source is paywalled or blocked) |
| Backups | AWS Backup cross-region copy rules; RDS automated backup replication (gated: unconfirmed, source is paywalled or blocked) |
| DNS/certs | ACM certificates requested in the DR region ahead of time (CloudFront certs stay in us-east-1) (gated: unconfirmed, source is paywalled or blocked) |

## Prepare the region
- Service quotas raised to production levels in the DR region (vCPU, EIPs, load balancers).
- Bootstrap stacks (CDK bootstrap, StackSets admin/execution roles), networking (VPC, TGW attachments, DX/VPN) pre-deployed: networking is slow to create and hard to change under pressure.
- Pipelines able to target the DR region with no edits.

## Drill
1. In a test account, deploy the full stack to the DR region from scratch; time each phase.
2. Restore the latest backups into it; run smoke tests.
3. Record time to working service vs RTO; fix the slowest step (often database restore size or manual DNS/cert steps).

## Gotchas
- Stateful resources with `DeletionPolicy: Retain` and fixed names collide on re-deploy; parameterise names.
- Cross-stack exports and SSM parameters must exist in the DR region before dependent stacks.
- CloudFormation in a new region still needs the same IAM capabilities and deploy roles.

## Verify
- [ ] Last rebuild drill completed under RTO with only pipeline-driven steps.
- [ ] Artifact replication monitored (ECR replication status, backup copy job alarms).

## Checked

2026-10-28

Confirmed: AWS::Region pseudo parameter and Fn::GetAZs for a given Region (CloudFormation User Guide pages).

Removed: prose-only sources replaced with the CloudFormation pages.

Gated: the artifact replication table (Image Builder, ECR, KMS multi-Region keys, Secrets Manager replicas, Backup copy rules, ACM/CloudFront note): none of these guides were fetched.

Method: documentation only; no commands were run.
