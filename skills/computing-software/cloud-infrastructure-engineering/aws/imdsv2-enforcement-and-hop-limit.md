---
id: computing-software.cloud-infrastructure-engineering.aws.imdsv2-enforcement-and-hop-limit
name: imdsv2-enforcement-and-hop-limit
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, imdsv2, imdsv2-enforcement, http-tokens-required, imds-hop-limit, ssrf, instance-metadata]
level: practitioner
status: docs-checked
description: "Enforce IMDSv2 across an EC2 fleet: find v1 callers with MetadataNoToken, set account defaults and AMI flags, hop limit 2 for containers, and SCP/Config guardrails."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-metadata-transition-to-version-2.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-IMDS-new-instances.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-options.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html", "https://docs.aws.amazon.com/config/latest/developerguide/ec2-imdsv2-check.html", "https://docs.aws.amazon.com/securityhub/latest/userguide/ec2-controls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enforcing IMDSv2 and the hop limit

**Why:** IMDSv1 lets an SSRF bug read role credentials with a single GET. IMDSv2 requires a
PUT-obtained session token, which SSRF and open proxies generally can't do.

## 1. Find who still uses v1
CloudWatch metric `MetadataNoToken` (namespace `AWS/EC2`, per instance) counts v1 calls.
```bash
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name MetadataNoToken \
  --dimensions Name=InstanceId,Value=i-123 --statistics Sum --period 86400 \
  --start-time $(date -u -d '-14 days' +%FT%TZ) --end-time $(date -u +%FT%TZ)
```
Non-zero means software on that instance still calls IMDSv1: update to IMDSv2-compatible AWS CLI and SDK
versions. The open-source IMDS Packet Analyzer identifies and logs IMDSv1 calls during boot and runtime.
The `ImdsV1Enabled` metric is published from configuration, so it also finds instances that still allow IMDSv1
when no calls are made. After you require IMDSv2, `MetadataNoTokenRejected` counts rejected IMDSv1 attempts
(the two call metrics are mutually exclusive per instance).

## 2. Switch instances
```bash
aws ec2 modify-instance-metadata-options --instance-id i-123 \
  --http-tokens required --http-put-response-hop-limit 2 --http-endpoint enabled
```
The change takes effect immediately on a running instance; no restart is needed. The PUT response hop limit
defaults to 1 and can be 1 to 64. A hop limit of 1 can cause issues in container environments, so AWS recommends
2 where containers need IMDS; keep 1 where nothing should reach it beyond the host.

## 3. Make it the default
- Account/region default for new launches:
  `aws ec2 modify-instance-metadata-defaults --http-tokens required --http-put-response-hop-limit 2`
- Enforce it per Region: `aws ec2 modify-instance-metadata-defaults --http-tokens-enforced enabled`. Launches that
  leave IMDSv1 enabled then fail, and IMDSv1 cannot be re-enabled on instances that have it off; existing
  instances with IMDSv1 enabled are not changed. Restrict `ec2:ModifyInstanceMetadataDefaults` with IAM so the
  enforcement cannot be reversed. Organizations declarative policies can set the same defaults org-wide.
- AMI flag: `aws ec2 register-image ... --imds-support v2.0` for new AMIs or `aws ec2 modify-image-attribute`
  for existing ones (instances from it default to v2). Amazon Linux 2023 AMIs already set this and AL2023
  disables IMDSv1 by default.
- Launch templates: `MetadataOptions={HttpTokens=required,HttpPutResponseHopLimit=2}`.

## 4. Guardrails
- SCP denying `ec2:RunInstances` unless `ec2:MetadataHttpTokens` = `required`, and denying
  `ec2:ModifyInstanceMetadataOptions` for non-admins.
- Condition `ec2:RoleDelivery` with value 2.0 in IAM policies or an SCP, so API calls made with credentials
  obtained through IMDSv1 get `UnauthorizedOperation`.
- The condition keys `ec2:MetadataHttpTokens`, `ec2:MetadataHttpPutResponseHopLimit` and
  `ec2:MetadataHttpEndpoint` govern `RunInstances` and `ModifyInstanceMetadataOptions`.
- Config managed rule `ec2-imdsv2-check` (NON_COMPLIANT when HttpTokens is optional); Security Hub CSPM controls
  EC2.8 (instances) and EC2.170 (launch templates).

## v2 call reference
```bash
TOKEN=$(curl -sX PUT http://169.254.169.254/latest/api/token -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600')
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id
```

## Gotchas
- A hop limit of 1 can cause issues for workloads in containers; see "Instance metadata access considerations" in the EC2 User Guide.
- Old agents (some third-party monitoring/backup) break; update them before enforcing.

## Verify
- [ ] `MetadataNoToken` = 0 for 14 days before switching each fleet.
- [ ] `aws ec2 describe-instances --query 'Reservations[].Instances[?MetadataOptions.HttpTokens!=\`required\`].InstanceId'` returns nothing.
- [ ] `curl http://169.254.169.254/latest/meta-data/` without token returns 401.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide pages "Transition to using Instance Metadata Service Version 2", "Use the Instance Metadata Service" (configuring-instance-metadata-service), "Configure the Instance Metadata Service options", "Configure instance metadata options for new instances" and "Instance metrics"; AWS Config rule ec2-imdsv2-check page; Security Hub CSPM EC2 controls page; botocore EC2 model (ModifyInstanceMetadataOptions, ModifyInstanceMetadataDefaults HttpTokensEnforced).
Confirmed: MetadataNoToken, MetadataNoTokenRejected and ImdsV1Enabled in the AWS/EC2 namespace; no-restart behaviour; hop limit default 1 and range 1-64; 401 for tokenless requests when tokens are required; imds-support v2.0; the three condition keys and ec2:RoleDelivery 2.0; account default and enforcement settings; Config rule and Security Hub controls EC2.8 and EC2.170.
Removed: the statement about SDKs "released since ~2019" and the EKS IRSA and Pod Identity detail, which the pages do not cover.

Method: documentation only; no commands were run.
