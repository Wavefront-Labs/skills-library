---
id: computing-software.cybersecurity-defensive.pomerium.session-recording-audit-chain
name: session-recording-audit-chain
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [chain-of-custody, worm-semantics, user-hmac-id, access-id, integrity-checks]
level: sme
status: docs-checked
description: "Audit Pomerium session recordings: WORM access pattern, digest checks, Enterprise audit log fields, correlating cloud storage logs, and integrity red flags."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/session-recording/auditing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enterprise feature. Chain of custody combines storage access patterns, Enterprise audit logs and cloud audit logs.

**WORM**: Core writes each object once and never deletes; Enterprise reads only. Guarantees are as strong as the bucket, so configure encryption, object locking and retention.

**Digest checks**: the Envoy extension sends data plus a digest to the control plane; Pomerium verifies it, PUTs with a digest header, and blob storage writes atomically. Any mismatch fails the upload.

**Enterprise audit log** (one entry per bucket or recording access): `access_id`, `access_type` (`recording`, `metadata`, `bucket`, `download`), `deny`, `success`, `reason`, `recording_format`, `object_key`, `source_ip`, `user_agent`, `user_role`, `user_email`, `user_id`, `user_hmac_id`, `user_session_start`, `user_session_exp`, `datasource`.

**Correlate with the cloud**
- GCS: enable Data Access logs (`ADMIN_READ`, `DATA_READ`, `DATA_WRITE`); headers `x-goog-custom-audit-pomerium-access-id` and `x-goog-custom-audit-pomerium-user` (`u=` HMAC).
- S3: server access logging or CloudTrail data events; URI parameter `pomerium_access_id`; user agent `app/<Pomerium-Version>-<Timestamp>--u-<hmac_user_id>--`. Special characters become `-` in S3 logs, and HEAD requests carry no IDs.
- Azure: `StorageBlobLogs`, `ClientRequestId` is the access ID, `UserAgentHeader` holds the HMAC.

The HMAC uses the Enterprise shared secret; keep the previous secret after rotation.

**Red flags**: more than one revision of a recording object; storage reads without Pomerium annotations; an `access_id` or `user_hmac_id` matching no Enterprise log.

## Checked

2026-11-04. Read the Session Recording Auditing page: WORM table, digest chain, audit log fields and access types, GCS, S3 and Azure correlation fields, S3 character and HEAD caveats, and the three integrity criteria all confirmed. Nothing removed.

Method: documentation only; no commands were run.
