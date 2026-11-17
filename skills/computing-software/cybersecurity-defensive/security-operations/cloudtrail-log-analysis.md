---
id: computing-software.cybersecurity-defensive.security-operations.cloudtrail-log-analysis
name: cloudtrail-log-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [log-analysis, cloudtrail-log-analysis, aws, useridentity, athena, assumerole-chains, cloud-investigation, cloudtrail]
level: practitioner
status: docs-checked
description: "Investigate AWS activity in CloudTrail: userIdentity types, following AssumeRole chains via accessKeyId, high-signal API calls, error codes and Athena queries."
sources: ["https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html", "https://docs.aws.amazon.com/athena/latest/ug/cloudtrail-logs.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudTrail log analysis for investigations

## Who did it: userIdentity
- `type`: `Root`, `IAMUser`, `AssumedRole` (temporary credentials from an STS AssumeRole call), `Role`, `FederatedUser`
  (GetFederationToken), `AWSAccount` (another account assumed a role you own), `AWSService`, `IdentityCenterUser`,
  `BuilderIdUser`, `Directory`, `Unknown`.
- `arn`: for AssumedRole, `arn:aws:sts::<acct>:assumed-role/<role>/<session-name>`.
- `accessKeyId`: the credential used. AWS's temporary-credential example shows an `ASIA...` key.
- `sessionContext.sessionIssuer`: the role behind the session; `sessionContext.attributes` holds `mfaAuthenticated`
  and `creationDate`. For actions by a product provider with delegated access, `invokedByDelegate.accountId` is the provider's account.
- `sourceIPAddress`: the requester's address; for services in AWS only the DNS name is shown, and for events
  originated by AWS it is usually `AWS Internal/#`.

## Following a chain
Attackers hop: stolen user key -> AssumeRole -> AssumeRole into another account. Trace with:
1. Find the `AssumeRole` event whose `responseElements.credentials.accessKeyId` equals the
   temporary key seen in suspicious events (the STS AssumeRole response returns a Credentials structure with an AccessKeyId).
2. Its `userIdentity` is the previous hop. Repeat until you reach a long-term IAM user key, a console login,
   or an SSO session. Cross-account hops need the trail of the other account.

## High-signal events
- Discovery: `GetCallerIdentity`, `ListBuckets`, `DescribeInstances`, `ListUsers` bursts from a new IP.
- Persistence: `CreateUser`, `CreateAccessKey`, `CreateLoginProfile`, `AttachUserPolicy`,
  `PutRolePolicy`, `UpdateAssumeRolePolicy`, new IAM Identity Center assignments.
- Defence evasion: `StopLogging`, `DeleteTrail`, `PutEventSelectors`, `DeleteDetector` (GuardDuty),
  `DisableSecurityHub`, `DeleteFlowLogs`.
- Exfil/impact: `GetObject` spikes (data events only), `PutBucketPolicy` making buckets public,
  `ModifySnapshotAttribute`/`ModifyImageAttribute` sharing to foreign accounts, `RunInstances` of
  large GPU types (mining), `CreateKeyPair`/`ImportKeyPair`.
- `errorCode` / `errorMessage`: top-level fields for some services; other services put error information in `responseElements`.

## Athena query
```sql
SELECT eventtime, eventsource, eventname, sourceipaddress, useragent, errorcode,
       useridentity.arn, useridentity.accesskeyid
FROM cloudtrail_logs
WHERE useridentity.accesskeyid = 'ACCESS_KEY_ID'
  AND eventtime > '2026-10-01T00:00:00Z'  -- adjust to the incident window
ORDER BY eventtime;
```
The Athena guide covers creating the table from the CloudTrail console, manual partitioning, an organisation-wide
trail table and partition projection. CloudTrail Lake offers SQL queries across accounts, Regions and dates inside
the CloudTrail console without Athena.

## Gotchas
- Data events are not logged by default for a trail or event data store; each resource type must be added
  beforehand, or object-level activity (such as S3 `GetObject`) is invisible.
- Event history shows management events only, for the past 90 days, one Region and one account at a time, with one
  attribute filter plus a time range; it does not aggregate across an organisation. Create a trail or event data store
  for a longer or wider record.

## Verify
Reconstruct a known admin session end to end (login to actions) to confirm your queries and
partitions return complete data before trusting a negative result.

## Checked
Checked 2026-11-08 against the AWS CloudTrail User Guide (userIdentity element, record contents, Event history,
concepts: data events default) and the Athena CloudTrail page. API operation names in the high-signal list were
confirmed to exist in the botocore models for cloudtrail, iam, sts, ec2, s3, guardduty and securityhub; whether they
are worth alerting on is analyst judgement. Removed as not confirmed: AKIA prefix meaning, session names carrying a
human identity, the 5-15 minute delivery delay, global services logging in us-east-1, the AccessDenied enumeration
reading, and the Security Incident Response whitepaper source (page returned empty).
Method: documentation only; no commands were run.
