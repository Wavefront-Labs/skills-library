---
id: computing-software.cloud-infrastructure-engineering.google-cloud.responding-to-a-leaked-service-account-key
name: responding-to-a-leaked-service-account-key
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, service-accounts, leaked-service-account-key, exposed-key-response, incident-response, key-disable, compromised-credentials]
level: practitioner
status: docs-checked
description: "Contain a leaked GCP service account key: disable it, scope the blast radius from audit logs by key ID, revoke persistence, rotate, and handle Google's exposed-key notification."
sources: ["https://cloud.google.com/iam/docs/keys-disable-enable", "https://cloud.google.com/docs/security/compromised-credentials", "https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts", "https://cloud.google.com/sdk/gcloud/reference/logging/read", "https://cloud.google.com/sdk/gcloud/reference/asset/analyze-iam-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responding to a leaked service account key

Google occasionally detects exposed keys, for example in a public repository. The
`iam.serviceAccountKeyExposureResponse` constraint sets the response: `DISABLE_KEY` automatically
disables the key, writes a Cloud Audit Logs event and notifies project owners and security contacts
(Essential Contacts). If the constraint is unset, the behaviour defaults to `DISABLE_KEY`. Google
recommends `DISABLE_KEY` over `WAIT_FOR_ABUSE`. The constraint cannot be merged with a parent policy;
replace the parent policy to enforce it.

## 1. Contain (minutes)
```bash
SA=app@<P>.iam.gserviceaccount.com; KEY=<KEY_ID>   # private_key_id from the JSON
gcloud iam service-accounts keys disable $KEY --iam-account=$SA
# if key ID unknown or several keys: disable the SA (breaks all workloads using it)
gcloud iam service-accounts disable $SA
```
A disabled key can be re-enabled; delete the key after investigation.

## 2. Scope
Search Cloud Audit Logs for activity by the compromised identity, org-wide:
```bash
gcloud logging read --organization=<ORG> --freshness=30d --format=json '<FILTER_FOR_THE_KEY>'
```
Build the filter from the audit log `authenticationInfo` fields (see the compromised-credentials guide).
If the identity had impersonation privileges, also search for
`protoPayload.authenticationInfo.serviceAccountDelegationInfo.firstPartyPrincipal.principalEmail`
matching it. Viewing Data Access logs needs `roles/logging.privateLogViewer`.
Check what the SA can reach:
`gcloud asset analyze-iam-policy --organization=<ORG> --identity=serviceAccount:$SA`.

## 3. Remove persistence
Look in the timeline for new keys (`CreateServiceAccountKey`), new SAs, IAM grants (`SetIamPolicy`),
new VMs or functions, startup-script metadata and OAuth clients. Revert each; delete attacker-created keys and SAs.

## 4. Recover
Issue a replacement credential, ideally moving the workload to Workload Identity Federation or an
attached SA. Delete the leaked key. Purge it from git history and any CI caches.

## Gotchas
- Active bearer tokens are valid for up to one hour; the compromised-credentials guide lists steps to block them sooner.
- A key in a public repo means assume compromised even if logs show nothing.

## Verify
- [ ] Key state is disabled or deleted; no API calls with that key after the containment time.
- [ ] Exposure response constraint enforced (not `WAIT_FOR_ABUSE`) at the org root.

## Checked
Date: 2026-10-31. Confirmed in the restricting-service-accounts page (constraint name, `DISABLE_KEY`
behaviour, default since June 2024, notification recipients, merge rule), the compromised-credentials guide
(one hour token validity, delegation-info log field, Private Logs Viewer for Data Access logs), the keys
disable/enable page, and the `gcloud logging read` and `gcloud asset analyze-iam-policy` references (flags
`--organization`, `--freshness`, `--format`, `--identity`). Removed unconfirmed claims: the exact
log filter field for the key name and the jq pipeline, "Google scans GitHub/GitLab", billing-spike advice.
Method: documentation only; no commands were run.
