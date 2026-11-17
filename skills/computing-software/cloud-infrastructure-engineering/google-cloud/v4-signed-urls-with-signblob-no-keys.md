---
id: computing-software.cloud-infrastructure-engineering.google-cloud.v4-signed-urls-with-signblob-no-keys
name: v4-signed-urls-with-signblob-no-keys
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-storage, signed-urls, v4-signing, signblob, iam-credentials, keyless, service-account-impersonation]
level: practitioner
status: docs-checked
description: "Generate Cloud Storage V4 signed URLs without service account keys via the IAM signBlob API or gcloud impersonation, with upload URLs, header rules and lifetime limits."
sources: ["https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers", "https://cloud.google.com/storage/docs/access-control/signed-urls", "https://cloud.google.com/iam/docs/reference/credentials/rest/v1/projects.serviceAccounts/signBlob", "https://cloud.google.com/sdk/gcloud/reference/storage/sign-url"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# V4 signed URLs with signBlob (no keys)

Signing normally needs a service account private key. Without one (Cloud Run, GKE, CI), the signer
can call the IAM Credentials `signBlob` method on a service account instead.

## 1. Permission
The caller needs the Service Account Token Creator role (`roles/iam.serviceAccountTokenCreator`), which includes
`iam.serviceAccounts.signBlob`, on the service account that signs. For a runtime that signs as itself:
```bash
SA=uploads-api@<P>.iam.gserviceaccount.com
gcloud iam service-accounts add-iam-policy-binding $SA --member=serviceAccount:$SA --role=roles/iam.serviceAccountTokenCreator
```
The signing service account also needs access to the objects the URL will reach (grant it the Storage roles
your use case needs). The `signBlob` resource name is `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`; the `-` wildcard is required.

## 2. Client libraries
The Cloud Storage helper-libraries page shows each language's options. In Go, `storage.SignedURL`
accepts a private key, a Google Access ID whose service account has `iam.serviceAccounts.signBlob`,
or a custom `SignBytes` function. Read the page's example for your language rather than copying a key-based sample.

## 3. CLI
```bash
gcloud storage sign-url gs://<B>/reports/q3.pdf --duration=10m --impersonate-service-account=$SA
gcloud storage sign-url gs://<B>/uploads/x.bin --http-verb=PUT --duration=1h \
  --headers=content-type=application/octet-stream --impersonate-service-account=$SA
```
`--duration` defaults to 1 hour (3600 s).

## Gotchas
- The longest V4 expiration is 604800 seconds (7 days). With `gcloud storage sign-url` and a system-managed key (impersonation), the maximum is **12 hours**; 7 days needs `--private-key-file` or an account authorized with `gcloud auth activate-service-account`.
- Headers you sign (for example `Content-Type`) must be sent by the client exactly; the docs' PUT examples show `curl -X PUT -H 'Content-Type: ...' --upload-file`.
- `signBlob` is an API call: avoid signing per request for hot objects.

## Verify
- [ ] `curl -X PUT -H 'Content-Type: application/octet-stream' --upload-file a.bin "<url>"` succeeds when the signed header matches.
- [ ] No `private_key` exists anywhere in the service's config or secrets.

## Checked

2026-10-28. Confirmed against: the Cloud Storage signed URLs page (604800 second maximum), the helper-libraries page (Token Creator role, `iam.serviceAccounts.signBlob`, Go `SignedURL` options, PUT example with Content-Type), the `gcloud storage sign-url` reference (default 3600 s, 12 hour limit with system-managed keys, 7 days with a key file) and the IAM Credentials signBlob reference (resource name format).

Removed: the Python snippet using `access_token` and `service_account_email` and the claim that Node signs automatically (not on the pages read), `iamcredentials.googleapis.com` and `storage.objectAdmin` instructions, the bucket CORS command, the quota remark, and the `SignatureDoesNotMatch` and 403 outcomes. The old 7-day lifetime gotcha was corrected for the signBlob path.

Method: documentation only; no commands were run.
