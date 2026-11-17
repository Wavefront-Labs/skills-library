---
id: computing-software.cryptography-implementation.key-management.auditing-key-usage
name: auditing-key-usage
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-management-policy, key-usage-audit, cloudtrail, cloud-audit-logs, kms-logging, anomaly-detection, hsm-audit-log]
level: advanced
status: draft
description: "Log and review every use of a key: KMS CloudTrail/Cloud Audit Logs fields, HSM audit logs, alerts for unusual callers and volumes, and tamper-evident retention."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/logging-using-cloudtrail.html", "https://cloud.google.com/kms/docs/audit-logging", "https://learn.microsoft.com/en-us/azure/key-vault/general/logging", "https://csrc.nist.gov/pubs/sp/800/57/pt2/r1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Auditing key usage

Keys in a KMS or HSM give you something plaintext keys never do: a log of each
use. That log is how you detect misuse and how you scope a compromise ("which
records were decrypted by the stolen role between Tuesday and Thursday?").

## Turn it on

- **AWS KMS**: management events are in CloudTrail by default; `Decrypt`,
  `Encrypt`, `GenerateDataKey`, `Sign` are data-plane events recorded as
  management events for KMS. Ensure an org trail to a separate log account
  with S3 Object Lock.
- **Google Cloud KMS**: Admin Activity logs are always on; **Data Access logs
  for cloudkms.googleapis.com must be enabled** explicitly (IAM audit config
  `DATA_READ`, `DATA_WRITE`) or you will not see Decrypt calls.
- **Azure Key Vault**: diagnostic setting `AuditEvent` to Log Analytics / storage.
- **HashiCorp Vault**: enable an audit device (`vault audit enable file
  file_path=...`); Vault refuses requests if all audit devices fail.
- **HSMs**: enable the appliance audit log and forward via syslog; Luna and
  nShield sign audit records for tamper evidence.

## What to record and keep

Caller identity (role/session, source IP, workload), key id/version,
operation, encryption context (KMS) - which tells you *what* was decrypted -,
result, timestamp. Retain per policy (often 1 year hot, 7 years cold), in
a different account/project than the key users, write-once.

Put a meaningful encryption context (`tenant`, `table`, `record_id`) on each
KMS call; it is logged in clear and turns the log into a data-access audit.

## Alerts worth having

- Decrypt from an identity that never used this key before.
- Volume spike (e.g. > 10x the 7-day baseline of Decrypt per caller).
- Key policy changes, grants created, `DisableKey`, `ScheduleKeyDeletion`,
  `ImportKeyMaterial`.
- Use of keys marked decrypt-only for encryption, or of retired key versions.
- Access denied bursts (probing).

```sql
-- Athena over CloudTrail: top decrypt callers per key, last 24h
SELECT useridentity.arn, json_extract_scalar(requestparameters,'$.keyId') k, count(*) n
FROM cloudtrail WHERE eventsource='kms.amazonaws.com' AND eventname='Decrypt'
  AND eventtime > to_iso8601(current_timestamp - interval '1' day)
GROUP BY 1,2 ORDER BY n DESC LIMIT 50;
```

## Verify

- [ ] A test Decrypt appears in the log with caller and context within minutes.
- [ ] Logs land in a separate account/project with immutability.
- [ ] Alert fires on a test `ScheduleKeyDeletion` and a new-caller decrypt.
