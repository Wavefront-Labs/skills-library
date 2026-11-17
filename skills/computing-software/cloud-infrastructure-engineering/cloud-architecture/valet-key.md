---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.valet-key
name: valet-key
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-patterns, valet-key, pre-signed-url, presigned-post, sas-token, user-delegation-sas, signed-url, direct-upload, object-storage]
level: practitioner
status: docs-checked
description: "Let clients upload/download directly to object storage with scoped, short-lived tokens (pre-signed URLs, SAS, signed URLs): scope, expiry and post-upload validation."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/valet-key", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html", "https://learn.microsoft.com/azure/storage/common/storage-sas-overview", "https://cloud.google.com/storage/docs/access-control/signed-urls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Valet key

Offload bulk data transfer from your app servers: the app authorises the request and hands the
client a narrowly scoped, time-limited token for one resource. Do not use it when clients can
already authenticate to the backend directly, or when the app must process the data in flight.

## Steps
1. Client asks the API for an upload slot. The API authenticates and authorises the user and
   picks the object key itself (for example `uploads/<tenant>/<uuid>`); do not accept a
   client-supplied path.
2. Issue the token with the least permission: write-only for uploads, read-only for downloads,
   scoped to the one object, with a validity period.
   - AWS: presigned URL for an HTTP method (GET to download, PUT to upload). Its capabilities are
     limited by the permissions of the creator. With the S3 console, expiry is 1 minute to 12
     hours; with the CLI or SDKs, up to 7 days (IAM user, Signature Version 4). A URL made with
     temporary credentials (an IAM role session) expires when those credentials expire, even if
     a longer expiry was requested.
   - Azure: prefer a user delegation SAS (signed with Microsoft Entra credentials) over a service
     or account SAS, which are signed with the storage account key. Microsoft recommends this
     for superior security.
   - Google Cloud Storage: V4 signed URL, longest expiry 604800 seconds (7 days).
3. Keep expiry near-term; Azure advises short-lived SAS and allowing for clock skew on the end time.
   Set a start time slightly earlier than server time (pattern guidance).
4. Validate and, if needed, sanitise everything uploaded before use: a holder of the key could
   upload malicious data. Enforce TLS for clients talking to the store directly.
5. Browser clients need CORS enabled on the store to use the key from another domain.

## Gotchas
- Presigned URLs are bearer tokens that grant access to whoever holds them; protect them. S3
  bucket policies can use the `s3:signatureAge` condition to reject old signatures.
- Azure: a service SAS can be revoked via a stored access policy (limit of five per container)
  without regenerating account keys; user delegation and account SAS must be ad hoc (no stored
  access policy).
- If the client never reports completion and only expiry limits the key, you cannot count or limit uploads/downloads; the server can invalidate the key once the client signals completion.
- You are billed for usage through a SAS, so limit permissions and lifetime.
- GCS resumable uploads usually need no signed URL for the data PUTs: the session URI acts as the token.

## Verify
- [ ] Token cannot write a different key or be used for a different action.
- [ ] Expired token is rejected.
- [ ] Uploaded file is not served to others until validated.

## Checked
2026-11-08
Method: documentation only; no commands were run.
Confirmed against the Azure Architecture Center Valet Key pattern, the S3 presigned URL page, the Azure Storage SAS overview and the GCS signed URLs page. Removed unconfirmed claims: presigned POST with content-length-range, "PUT cannot enforce size", GCS POST policy documents, `sp`/`se` parameter names, event-triggered malware scan and quarantine/clean layout, and the claim that account-key SAS is revocable only by key rotation (a stored access policy can revoke a service SAS).
