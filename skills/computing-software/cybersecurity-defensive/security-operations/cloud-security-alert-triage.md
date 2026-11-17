---
id: computing-software.cybersecurity-defensive.security-operations.cloud-security-alert-triage
name: cloud-security-alert-triage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [cloud-alert-triage, alert-triage, guardduty, defender-for-cloud, security-command-center, cloudtrail, cloud-security, soc]
level: practitioner
status: docs-checked
description: "Triage cloud security alerts (GuardDuty, Defender for Cloud, Security Command Center): establish the principal, origin and API activity, then decide contain or close."
sources: ["https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-active.html", "https://learn.microsoft.com/en-us/azure/defender-for-cloud/alerts-overview", "https://docs.cloud.google.com/security-command-center/docs/concepts-security-sources", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cloud security alert triage

## Where the alert comes from
- **AWS GuardDuty:** a finding is a notification that GuardDuty generates when it detects an
  indication of suspicious or malicious activity in an account. The finding-types list gives each
  type's impacted resource, data source and severity.
- **Microsoft Defender for Cloud:** alerts come from its workload protection plans. Severity is based
  on the specific trigger and the confidence that activity was malicious. High: high probability
  the resource is compromised, look at once. Medium: probably suspicious (often ML or
  anomaly-based, for example a sign-in from an unusual location). Low: might be benign or a blocked
  attack (for example log clearing, which admins also do routinely). Informational alerts can matter
  as part of an incident. Alerts correlate into incidents (collections of related alerts) and
  map to the MITRE ATT&CK matrix. Alerts show in the portal for 90 days.
- **Google Security Command Center:** findings come from built-in services such as Security
  Health Analytics (managed scans for misconfigurations) and Event Threat Detection.

## First five minutes
1. **Who:** the principal (IAM user, role session, managed identity, service account). In a CloudTrail
   record, `userIdentity` carries `type` (such as Root, IAMUser, Role), `principalId` and `arn`.
   Decide whether it is a human, a workload or a third-party integration.
2. **From where:** `sourceIPAddress` and `userAgent` on the CloudTrail event. A human principal
   suddenly appearing from a new network or anonymising service is a strong signal.
3. **What:** the API calls in the window (`eventName`, `eventTime`, `errorCode`): enumeration,
   persistence (new users or access keys, policy attachments), defence evasion (stopping
   logging), and impact (instances launched in regions the account never uses).
4. **Exposure:** is the resource reachable from the internet, does it hold sensitive data, what can
   the principal reach.
5. **Change context:** change ticket, CI pipeline run, known automation.

## Query (CloudTrail Lake or Athena style)
```sql
SELECT eventtime, eventname, sourceipaddress, useragent, errorcode
FROM cloudtrail WHERE useridentity.arn LIKE '%<ROLE>%' AND eventtime > now() - interval '24' hour
ORDER BY eventtime;
```
Table and column naming depends on how you set up Athena or Lake; the field names come from the
CloudTrail record contents. Use your Azure Activity and GCP Cloud Audit Logs equivalents for the
same principal-and-window question.

## Example GuardDuty finding types (names, resource, severity from the list)
- `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS` (IAM; High) and
  `.InsideAWS` (IAM; High): treat as credential theft until the principal's activity proves
  otherwise.
- `Recon:IAMUser/TorIPCaller` and `Recon:IAMUser/MaliciousIPCaller` (IAM; Medium).
- `Stealth:IAMUser/CloudTrailLoggingDisabled` (IAM; Low): low severity, but logging being turned
  off in the middle of an incident is a significant change.
- `CryptoCurrency:EC2/BitcoinTool.B` (EC2; High; VPC flow log source) and `.B!DNS` (DNS logs).
Suppress only specific benign sources (for example a known scanner) by principal and finding type.

## Containment options
- AWS role sessions: the IAM console action "Revoke active sessions" attaches an
  `AWSRevokeOlderSessions` inline policy that denies all access to anyone who assumed the role
  before the revocation time (plus roughly 30 seconds of propagation margin). The same effect is
  available with a Deny policy using a `DateLessThan` condition on `aws:TokenIssueTime`. This
  denies every user of that role, and a service-linked role cannot be revoked this way; roles
  created from IAM Identity Center permission sets must be revoked in Identity Center.
- Other clouds: use the vendor's documentation for revoking tokens and disabling credentials; this
  page's sources do not cover those steps.
- Preserve evidence (snapshots, logs) before destroying a compromised resource.

## Verify
Case notes record principal, origin, API timeline, exposure, verdict and containment; suppression
rules for benign verdicts are scoped by principal and finding type, not global.

## Checked
2026-11-08. Confirmed against the GuardDuty active finding types page (finding names, resources,
severities), the Defender for Cloud alerts overview (severity definitions, incidents, 90 days),
the Security Command Center security sources page (Security Health Analytics), CloudTrail record
contents and userIdentity pages (`eventTime`, `eventName`, `sourceIPAddress`, `userAgent`,
`errorCode`, `type`, `principalId`, `arn`) and the IAM revoke-sessions page
(`AWSRevokeOlderSessions`, `aws:TokenIssueTime`, limits). Removed: the `sourceIdentity` tracing
advice, specific API names as "persistence/evasion" lists, the `AzureActivity` and
`protoPayload.authenticationInfo.principalEmail` queries, verdicts such as "almost always true
positive" and "Recon is benign", Azure refresh-token and service-principal revocation steps,
access-key deactivation and isolation security group steps (not on the cited pages).
Method: documentation only; no commands were run.
