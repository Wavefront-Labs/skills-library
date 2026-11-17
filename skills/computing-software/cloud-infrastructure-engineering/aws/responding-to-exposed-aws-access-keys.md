---
id: computing-software.cloud-infrastructure-engineering.aws.responding-to-exposed-aws-access-keys
name: responding-to-exposed-aws-access-keys
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, exposed-access-key, compromised-credentials, awscompromisedkeyquarantine, incident-response, iam, cloudtrail]
level: advanced
status: docs-checked
description: "Respond to a leaked IAM access key: the AWS quarantine policy, deactivate and rotate, scope the blast radius in CloudTrail, remove attacker resources, move to roles."
sources:
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
  - https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSCompromisedKeyQuarantineV3.html
  - https://docs.aws.amazon.com/health/latest/ug/cloudwatch-events-health.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responding to exposed AWS access keys

Access keys are long-term credentials for an IAM user or the root user; an access key ID plus its secret signs CLI and API requests. A user can have at most two access keys.

## 1. Signals
- AWS applies the managed policy `AWSCompromisedKeyQuarantineV3` (a newer version such as V4 may exist) when an IAM user's credentials are compromised or exposed publicly. It denies a long list of actions to limit fraud-related charges without affecting existing resources, including `ec2:RunInstances`, `iam:CreateUser`, `iam:CreateAccessKey`, `iam:CreateLoginProfile`, `s3:PutBucketPolicy`, `lambda:CreateFunction`, `organizations:LeaveOrganization`, `sts:GetSessionToken` and `sts:GetFederationToken`. Read the policy page for the full list.
- The policy page says not to remove it and to follow the instructions in the support case AWS creates for the event.
- AWS Health events can be routed with Amazon EventBridge rules to targets such as Lambda, SNS, SQS or Kinesis. Rules receive events for your own account only; use the Health organizational view for other accounts in an organization.
- Your own detection: CloudTrail to monitor access key use, and CloudWatch alarms for denied access attempts.

## 2. Contain (minutes)
Run these as an administrator identity, not as the quarantined user (the quarantine policy itself denies `iam:UpdateAccessKey`, `iam:DeleteAccessKey` and `iam:PutUserPolicy` to that user).
```bash
aws iam update-access-key --user-name ci-deploy --access-key-id <ACCESS_KEY_ID> --status Inactive
```
Do not remove the AWS quarantine policy; follow the support case. Credentials minted with the key (`GetSessionToken`, `GetFederationToken`, role sessions) are a follow-up item: find them in CloudTrail in the next step.

## 3. Scope (hours)
Search CloudTrail for the key ID across all regions and accounts (event history, an organization trail, or a query store you already have). Look for what the key did and for credentials or access it created: `CreateAccessKey`, `CreateUser`, `CreateLoginProfile`, `AssumeRole`, `GetSessionToken`, `GetFederationToken`. The quarantine policy's deny list is a useful checklist of high-risk actions to look for (instance launches, IAM changes, bucket policy changes, Lambda creation, leaving the organization).

## 4. Eradicate and recover
- Delete resources the attacker created: users, keys, roles, policies, instances in every region, Lambda functions, buckets or policy changes.
- Rotate the key: create a new one, update consumers, delete the old key. Better, replace long-term keys with temporary credentials such as IAM roles; AWS recommends this over creating access keys.
- Check billing for unexpected charges.
- Assume a secret that reached a public repository is permanently exposed, so rotation is mandatory.

## 5. Prevent
- Do not create access keys with root credentials, put keys in application files, or include credential files in the project area. Keys in the shared AWS credentials file are stored in plaintext.
- Review, update and delete access keys regularly.

## Verify
- [ ] Key inactive then deleted; no successful API calls from it after containment time (CloudTrail).
- [ ] Everything the attacker created is removed in every region and account.
- [ ] Root cause documented; workload moved off long-term keys.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the IAM access keys page (two-key maximum, plaintext credentials file, monitoring recommendations, roles preferred), the AWSCompromisedKeyQuarantineV3 policy page (description, do-not-remove note, deny list entries named above), and the AWS Health EventBridge page (targets, own-account scope). CLI command checked against the botocore model. Removed as not stated by the pages: the AWS_RISK_CREDENTIALS_EXPOSED event code and the EventBridge pattern, GuardDuty finding names, the aws:TokenIssueTime deny recipe, the CloudTrail Lake query, Access Analyzer and SCP advice, support-case billing steps, and the incident response whitepaper source (page unreadable).
