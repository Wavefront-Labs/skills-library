---
id: computing-software.digital-forensics-incident-response.incident-response-process.aws-incident-response
name: aws-incident-response
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [aws-incident-response, cloud-incident-response, cloudtrail, guardduty, iam, aws, dfir]
level: advanced
status: docs-checked
description: "Respond to AWS incidents: CloudTrail scope and log integrity, leaked key triage, revoking role sessions, GuardDuty instance credential findings, EC2 snapshot and IAM review."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html", "https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html", "https://github.com/aws-samples/aws-incident-response-playbooks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS incident response

**Goal:** contain, investigate and recover AWS account compromises. The AWS Security Incident Response Guide page
could not be read in this review; the practices below are limited to what the pages cited above state.

## Preparation that matters
- CloudTrail: a multi-Region trail is recommended (a single-Region trail shows only its own Region). Management
  events are logged by default; data events (S3 object reads, Lambda `Invoke`, and others) are not, and cost extra.
  Event history holds only the past 90 days of management events per Region.
- Enable log file integrity validation: CloudTrail hashes each log file (SHA-256) and delivers a signed hourly digest
  file to the trail's S3 bucket, so you can show logs were not changed or deleted.
- CloudTrail Lake event data stores allow SQL queries over events.
- GuardDuty, and a plan for who runs the playbooks (see the aws-incident-response-playbooks repository).

## Leaked access key playbook
1. Identify the key and principal: a GuardDuty finding, or `aws sts get-caller-identity` from the leaked key (only
   if counsel agrees).
2. Deactivate (not delete) the key: `aws iam update-access-key --user-name <u> --access-key-id <KEY_ID> --status Inactive`.
3. Investigate in CloudTrail for all calls by `userIdentity.accessKeyId`. See the responding-to-leaked-cloud-access-keys
   skill for `lookup-events` with the `AccessKeyId` attribute.
4. Look for persistence: `CreateUser`, `CreateAccessKey`, `CreateLoginProfile`, `AttachUserPolicy`,
   `CreateRole`/`UpdateAssumeRolePolicy` (trust changes), `CreateFunction`, `PutBucketPolicy`, `ModifySnapshotAttribute`.
5. Revoke sessions of any role assumed: IAM attaches an inline policy `AWSRevokeOlderSessions` that denies all actions
   for sessions issued before a time (about 30 seconds into the future when done from the console), via a
   `DateLessThan` condition on `aws:TokenIssueTime`. You need the `PutRolePolicy` permission; it affects all users of
   the role, cannot be done for a service-linked role, and sessions created after it are not affected. The
   Deny does not affect requests signed with an IAM user's long-term credentials. Cached CLI credentials may need
   clearing.

## Compromised EC2
- GuardDuty finding `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.InsideAWS` (credentials of an instance
  launch role used from another AWS account; High severity, Medium if the account is affiliated with yours) and its
  `.OutsideAWS` counterpart indicate stolen instance role credentials. Identify the remote account in
  `service.action.awsApiCallAction.remoteAccountDetails.accountId`; check `remoteAccountDetails.Affiliated`.
  GuardDuty stops generating the finding for a remote account once its model learns the activity as expected.
- Isolate by replacing the instance's security groups (`aws ec2 modify-instance-attribute --instance-id <ID> --groups
  <ISOLATION_SG>`), snapshot volumes (`aws ec2 create-snapshot --volume-id <ID>`), then analyse copies elsewhere.

## Gotchas
- CloudTrail Event history is management events only and 90 days.
- Event names may carry version suffixes; search accordingly.

## Verify
No API calls from compromised principals after containment; compare IAM against a pre-incident baseline
(`aws iam get-account-authorization-details`) for unexplained principals.

## Checked
2026-11-08. Confirmed: IAM "Revoke IAM role temporary security credentials" page (AWSRevokeOlderSessions,
aws:TokenIssueTime, PutRolePolicy, limits); GuardDuty IAM finding types page (InstanceCredentialExfiltration
InsideAWS/OutsideAWS, severity note, remote account fields); CloudTrail concepts (90-day event history, data events off
by default, multi-Region); log file integrity validation page (SHA-256, hourly signed digest); command names and
flags (check_commands.py) and API operation names (botocore). Removed (unconfirmed or unreadable source): object
lock, Security Hub, VPC flow logs, forensic account design, LiME/AVML memory capture, termination protection, IMDSv1
SSRF, the Athena query, and the specific "unused region" mining heuristic.
Method: documentation only; no commands were run.
