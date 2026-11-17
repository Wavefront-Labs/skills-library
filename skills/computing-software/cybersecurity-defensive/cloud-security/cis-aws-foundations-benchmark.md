---
id: computing-software.cybersecurity-defensive.cloud-security.cis-aws-foundations-benchmark
name: cis-aws-foundations-benchmark
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cis-aws-foundations, cis-benchmark, aws-security-hub, prowler, aws-baseline, cspm]
level: practitioner
status: draft
description: "Assess and maintain the CIS AWS Foundations Benchmark: IAM, logging, monitoring and networking controls, Security Hub standard and Prowler checks, and exceptions handling."
sources: ["https://www.cisecurity.org/benchmark/amazon_web_services", "https://docs.aws.amazon.com/securityhub/latest/userguide/cis-aws-foundations-benchmark.html", "https://github.com/prowler-cloud/prowler"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CIS AWS Foundations Benchmark

## Sections (v3/v4)
1. **IAM:** root account MFA and no access keys, no root use, MFA for console users, credentials unused 45 days disabled, one active access key per user, key rotation 90 days, IAM policies attached to groups/roles not users, no `*:*` admin policies, support role exists, IAM Access Analyzer enabled, IAM Identity Center/federation for users.
2. **Storage:** S3 Block Public Access, deny HTTP (`aws:SecureTransport`), EBS default encryption, RDS encryption and no public access, EFS encryption.
3. **Logging:** multi-region CloudTrail with log file validation, S3 bucket access logging for the trail bucket, KMS encryption of trails, Config enabled in all regions, VPC flow logs, S3 object-level logging for write/read events.
4. **Monitoring:** metric filters and alarms (or EventBridge/Security Hub equivalents) for unauthorised API calls, console sign-in without MFA, root use, IAM/CloudTrail/Config/KMS/S3 policy/security group/NACL/gateway/route/VPC changes, Organizations changes, Security Hub enabled.
5. **Networking:** no NACL/security group admin port ingress from 0.0.0.0/0 or ::/0, default security group restricts all traffic, least-access VPC peering routing, IMDSv2.

## Assess
- AWS Security Hub CSPM standard "CIS AWS Foundations Benchmark v3.0.0" across the organisation (delegated admin, central configuration).
- Prowler: `prowler aws --compliance cis_4.0_aws -M html json-ocsf` (multi-account with `--role`).
- Track a score per account; attach evidence exports for audits.

## Remediate
Most items are best fixed once at the org level: Control Tower/landing zone guardrails, org trail, Config
everywhere, SCPs, IAM Identity Center. Section 4 alarms can be satisfied with Security Hub/GuardDuty
alerting where your auditor accepts it.

## Exceptions
Document per control/account with risk acceptance and expiry (e.g. a public S3 website bucket); suppress in
Security Hub with a note.

## Verify
- [ ] Security Hub CIS score per account above target; failed controls ticketed.
- [ ] Prowler run in CI/schedule with results trended.
