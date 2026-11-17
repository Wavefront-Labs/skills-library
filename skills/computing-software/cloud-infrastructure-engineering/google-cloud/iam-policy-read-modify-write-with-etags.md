---
id: computing-software.cloud-infrastructure-engineering.google-cloud.iam-policy-read-modify-write-with-etags
name: iam-policy-read-modify-write-with-etags
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam, iam-policy-etag, set-iam-policy-etag, policy-version-3, setiampolicy, concurrency]
level: practitioner
status: docs-checked
description: "Change GCP IAM policies safely with read-modify-write: etags to prevent lost updates, policy version 3 for conditions, and add-binding vs set-iam-policy trade-offs."
sources: ["https://docs.cloud.google.com/iam/docs/policies", "https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM policy read-modify-write with etags

Allow policies are updated with a read-modify-write pattern (read, modify, write back). When
several systems write the same policy at once they can overwrite each other's changes. Every
allow policy has an `etag` that changes on each update; include it when you write. If the policy
changed since you read it, the etag no longer matches and the update fails (REST returns
`409 Conflict` with "There were concurrent policy changes. Please retry the whole
read-modify-write with exponential backoff.").

## gcloud flows
```bash
# small changes
gcloud projects add-iam-policy-binding <PROJECT_ID> --member=group:devs@example.com --role=roles/viewer
gcloud projects remove-iam-policy-binding <PROJECT_ID> --member=group:devs@example.com --role=roles/viewer

# bulk edit: get, edit, set (the etag inside the file is what protects you)
gcloud projects get-iam-policy <PROJECT_ID> --format=json > policy.json
#   edit policy.json, keep "etag" and "version"
gcloud projects set-iam-policy <PROJECT_ID> policy.json
```
On a concurrency failure, re-read, re-apply your diff and retry with exponential backoff. Never
strip the etag to force the write.

## Policy versions
- A request that names no version is treated as version 1. A policy without conditions is always returned as version 1, whatever version was requested.
- If the policy has conditions and the caller requested version 1 (or none), IAM returns a version 1 policy, so request version 3 (`options.requestedPolicyVersion: 3` in `getIamPolicy`) whenever conditions may exist.
- When you use IAM Conditions, always specify version 3 and always include the etag when setting a policy through a client library or REST. Without the etag IAM lets a version 1 policy overwrite a version 3 policy and deletes all its conditions.

## Gotchas
- Bindings for deleted principals show as `deleted:...` and, for service accounts, with a `?uid=<numeric-id>` suffix.
- Each allow policy can contain up to 1,500 principals, and up to 250 of them can be Google groups, Cloud Identity domains or Workspace accounts; grant to groups and review the quota page for current limits.

## Verify
- [ ] Concurrent writers retry on the conflict error and no grant disappears in the audit logs.

## Checked
2026-10-31. Confirmed against "Policies and versions" (read-modify-write risk, etag behaviour, 409 Conflict and message, version 1/3 rules, requestedPolicyVersion, etag required with conditions, deleted: prefix and ?uid= suffix, 1,500 principals, 250 groups/domains). gcloud flags checked against the command reference. Removed: the claim that add-iam-policy-binding retries internally, the Python client sample, the Terraform authoritative-resource note and the exact gcloud ABORTED error text (not confirmed in fetched pages).
Method: documentation only; no commands were run.
