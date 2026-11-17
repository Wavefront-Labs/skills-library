---
id: computing-software.cryptography-implementation.key-management.auditing-kms-key-usage-logs
name: auditing-kms-key-usage-logs
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, kms-audit-logs, cloudtrail, cloud-audit-logs, azure-monitor, key-usage-audit, aws-kms, google-cloud-kms, azure-key-vault, detection]
level: practitioner
status: docs-checked
description: "Audit KMS key usage with CloudTrail, Cloud Audit Logs and Key Vault diagnostics: enable data-access logs, query decrypt events, alert on anomalous principals."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/logging-using-cloudtrail.html", "https://cloud.google.com/kms/docs/audit-logging", "https://learn.microsoft.com/en-us/azure/key-vault/general/logging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing KMS key usage logs

## Turn logging on (defaults differ)
| Provider | Default | Action |
|---|---|---|
| AWS KMS | All KMS API calls are logged by CloudTrail unless excluded per trail | Ensure an org trail exists; do not exclude `kms.amazonaws.com` events unless volume forces it |
| Google Cloud KMS | Encrypt/decrypt calls are Data Access (DATA_READ) logs | Enable Data Access audit logs for `cloudkms.googleapis.com` |
| Azure Key Vault | Logging must be enabled | Enable logging so `AuditEvent` records go to a storage account (or Azure Monitor logs) |

## Queries
AWS (Athena over CloudTrail):
```sql
SELECT eventtime, useridentity.arn, eventname, sourceipaddress,
       json_extract_scalar(requestparameters, '$.encryptionContext.app') AS app
FROM cloudtrail_logs
WHERE eventsource = 'kms.amazonaws.com' AND eventname IN ('Decrypt','GenerateDataKey','ReEncrypt')
  AND json_extract_scalar(resources[1].arn, '$') LIKE '%key/1234abcd%'
ORDER BY eventtime DESC LIMIT 100;
```
GCP (Logs Explorer):
```
protoPayload.serviceName="cloudkms.googleapis.com" protoPayload.methodName="Decrypt"
resource.labels.key_ring_id="app-ring"
```
Azure: filter `AuditEvent` records on `operationName` `KeyDecrypt` or `KeyUnwrap`; `identity` and `callerIpAddress` identify the caller.

## Alerts worth having
- Decrypt by a principal never seen before for that key.
- Spike in Decrypt volume (bulk exfiltration via the key).
- Key policy, grant, disable or schedule-deletion events.
- Access from unexpected regions or source IPs.

## Encryption context as audit data
Put non-secret identifiers (tenant, table, record type) in the encryption context; it appears in logs and makes
per-tenant forensic queries possible.

## Checked

2026-10-31. Confirmed in AWS KMS CloudTrail page (all calls logged by default; exclusion per trail via kms.amazonaws.com), Google Cloud KMS audit logging (Data Access logs, DATA_READ covers Decrypt and Encrypt), Azure Key Vault logging (AuditEvent, KeyDecrypt, KeyUnwrap, identity, callerIpAddress). Removed: GCP default-off claim, DATA_WRITE, Azure KQL field names and diagnostic-setting wording, aws:SourceVpce.

Method: documentation only; no commands were run.

## Verify
- [ ] A test Decrypt appears in the log pipeline within the expected delay.
- [ ] Alert fires for a decrypt by an unapproved role in staging.
