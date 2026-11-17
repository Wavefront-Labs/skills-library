---
id: computing-software.digital-forensics-incident-response.incident-response-process.responding-to-leaked-cloud-access-keys
name: responding-to-leaked-cloud-access-keys
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [leaked-access-key, aws-incident-response, cloud-incident-response, secret-rotation, dfir]
level: advanced
status: docs-checked
description: "Respond to leaked AWS or GCP keys: deactivate without losing evidence, scope every API call by key ID in CloudTrail, find attacker-created resources and backdoors."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html", "https://github.com/aws-samples/aws-customer-playbook-framework"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responding to leaked cloud access keys

**Goal:** keys leaked in a public repo, CI log or compromised laptop must be neutralised quickly, and every call made
with them scoped.

## 1. Stop use, keep evidence
```bash
aws iam update-access-key --user-name <u> --access-key-id <KEY_ID> --status Inactive   # not delete yet
aws iam list-access-keys --user-name <u>
```
- An IAM user can have at most two access keys; the secret is retrievable only at creation, so a lost secret means
  delete and recreate (IAM User Guide, "Manage access keys for IAM users").
- Temporary credentials (STS sessions) already minted by the key are a separate problem: scope them from the
  CloudTrail records (step 2) and check the IAM and STS documentation for how to revoke sessions.
- GCP: `gcloud iam service-accounts keys disable` (service account key). For Azure, rotate the service principal
  secret or certificate.

## 2. Scope by key ID
```bash
aws cloudtrail lookup-events --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=<KEY_ID> --max-results 50
```
- `AccessKeyId` is one of the LookupAttributeKey values (with EventId, EventName, ReadOnly, Username,
  ResourceType, ResourceName, EventSource); `--max-results` is 1-50, so page with the next token.
- Event history is a record of the past 90 days of management events in an AWS Region, so look in every Region
  (attackers may use unused Regions). For older or data-event history query your trail's logs (for example with
  Athena or CloudTrail Lake) on the access key ID field.
- Also scope the sessions the key created (calls such as `GetSessionToken` and `AssumeRole`) and the calls made
  with those.
- Source the CloudTrail field `userIdentity.accessKeyId` and `sessionContext` details from the CloudTrail record
  reference when writing queries.

## 3. Find what the attacker created
- IAM: new users, access keys, login profiles, roles with external trust, policy attachments (`CreateUser`,
  `CreateAccessKey`, `CreateLoginProfile`, `AttachUserPolicy`, `CreateRole`, `UpdateAssumeRolePolicy`).
- Compute: `RunInstances`, Lambda `CreateFunction`.
- Data: S3 object reads appear only if data events are enabled (they are not logged by default, and extra charges
  apply); `PutBucketPolicy`; `ModifySnapshotAttribute` (snapshot sharing).
- Defence evasion: CloudTrail `StopLogging` and `DeleteTrail`.

## 4. Remediate
Delete attacker resources (after snapshot/evidence capture), delete the leaked key, rotate any
secrets the key could read, add secret scanning to repos/CI. The IAM page recommends temporary credentials such as
IAM roles instead of long-term access keys, and CloudTrail plus CloudWatch alarms for monitoring key use.

## Gotchas
- Event history shows management events only; data events must have been enabled before the incident.
- Deactivating first (rather than deleting) lets you confirm no business breakage and keeps the key ID in IAM.

## Verify
No API calls with the key or its derived sessions after containment time, in all Regions.

## Checked
2026-11-08. Confirmed: the aws iam, aws cloudtrail and gcloud commands and flags (check_commands.py); the
LookupAttributeKey enum and MaxResults 1-50 (botocore model); the API operation names used above (botocore models
for iam, ec2, cloudtrail, sts, s3, lambda); the two-key limit, secret retrievable once, and monitoring advice (IAM
User Guide access keys page); the 90-day management-event history and data events not logged by default (CloudTrail
concepts page). Removed (not confirmed in the cited pages): the explicit-deny/AWSDenyAll with aws:TokenIssueTime
step, the "ASIA" prefix claim, GPU-instance mining heuristics, and the ECS and GuardDuty-disabled indicators.
Method: documentation only; no commands were run.
