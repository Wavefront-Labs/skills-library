---
id: computing-software.cybersecurity-defensive.cloud-security.s3-exfiltration-investigation
name: s3-exfiltration-investigation
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [s3-exfiltration-investigation, s3-data-events, s3-server-access-logs, guardduty-s3-protection, data-breach-scoping, cloud-incident-response]
level: practitioner
status: draft
description: "Investigate suspected S3 data exfiltration: evidence sources, identifying principal and access path, scoping objects and bytes, Athena queries, containment and notification input."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html", "https://docs.aws.amazon.com/guardduty/latest/ug/s3-protection.html", "https://docs.aws.amazon.com/athena/latest/ug/cloudtrail-logs.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging-s3-info.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# S3 exfiltration investigation

## Evidence sources
| Source | Gives | Availability |
|---|---|---|
| CloudTrail data events (GetObject, ListObjects) | Principal, IP, user agent, object key, time | Only if data events were enabled beforehand |
| S3 server access logs | Requester, IP, key, bytes sent, HTTP status, also anonymous/public access | Only if enabled; best effort delivery |
| CloudTrail management events | Policy changes (PutBucketPolicy, PutBucketAcl, PutPublicAccessBlock deletions), key creation for the principal | Always (90 days in Event history) |
| GuardDuty S3 Protection findings | Anomalous behaviour (Exfiltration:S3/AnomalousBehavior, Discovery:S3/...) | If enabled |
| VPC Flow Logs / endpoint policies | Network path (via VPC endpoint or internet) | If enabled |
| Macie | What sensitive data the objects contain | For scoping impact |

## Steps
1. Identify the access path: which principal (IAM user key, role session, presigned URL, public bucket/ACL, cross-account role).
2. Query object access for the window:
```sql
SELECT requester, remoteip, operation, key, SUM(bytessent) AS bytes, COUNT(*) AS n
FROM s3_access_logs_db.prod_customer_data
WHERE operation = 'REST.GET.OBJECT' AND httpstatus = '200'
  AND parse_datetime(requestdatetime,'dd/MMM/yyyy:HH:mm:ss Z') BETWEEN timestamp '2026-10-10 00:00:00 UTC' AND timestamp '2026-10-18 00:00:00 UTC'
GROUP BY requester, remoteip, operation, key ORDER BY bytes DESC
```
3. Compare to baseline (normal readers, volumes); list distinct keys accessed by the suspicious principal = **scope**.
4. Map keys to data classification (Macie results, object tags) for notification decisions.
5. Trace upstream: how the principal was compromised (CloudTrail for key creation, console logins, leaked key in repo).

## Contain
Disable/deactivate access keys, revoke role sessions (`AWSRevokeOlderSessions` inline deny by `aws:TokenIssueTime`), fix bucket policy/ACL/Block Public Access, rotate presigning credentials, add RCP/endpoint policy restrictions.

## Gotchas
- Without data events or access logs you can show who *could* access, not what was read - say so in the report.
- Presigned URLs show the signing principal as requester, not the downloader; IPs matter.

## Verify
- [ ] Scope report: principal, window, object list, bytes, data classes, confidence level.
