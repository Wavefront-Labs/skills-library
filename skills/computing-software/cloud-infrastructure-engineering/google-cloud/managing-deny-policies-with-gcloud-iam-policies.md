---
id: computing-software.cloud-infrastructure-engineering.google-cloud.managing-deny-policies-with-gcloud-iam-policies
name: managing-deny-policies-with-gcloud-iam-policies
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam-deny-policies, gcloud-iam-policies, deny-policy-attachment-points, deny-admin, url-encoded-attachment-point]
level: practitioner
status: docs-checked
description: "Create, list, update and delete IAM deny policies at organization, folder and project attachment points with gcloud iam policies, including URL-encoding and the denyAdmin role."
sources: ["https://cloud.google.com/iam/docs/deny-access", "https://cloud.google.com/sdk/gcloud/reference/iam/policies", "https://cloud.google.com/iam/docs/deny-overview#attachment-points"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing deny policies with gcloud iam policies

Deny policies attach to org, folder or project (each resource can have up to 500 deny policies, with 500 deny rules across them).
Viewing needs `roles/iam.denyReviewer` and managing needs `roles/iam.denyAdmin` on the organisation.

## Attachment point encoding
```bash
ORG_AP=cloudresourcemanager.googleapis.com%2Forganizations%2F123456789012
FOLDER_AP=cloudresourcemanager.googleapis.com%2Ffolders%2F987654321
PROJ_AP=cloudresourcemanager.googleapis.com%2Fprojects%2F<PROJECT_ID>
```

## Create
```json
// deny-sa-keys.json
{
  "displayName": "No SA key creation outside the security team",
  "rules": [{
    "denyRule": {
      "deniedPrincipals": ["principalSet://goog/public:all"],
      "exceptionPrincipals": ["principalSet://goog/group/gcp-security-admins@example.com"],
      "deniedPermissions": ["iam.googleapis.com/serviceAccountKeys.create"]
    }
  }]
}
```
```bash
gcloud iam policies create deny-sa-keys --attachment-point=$ORG_AP --kind=denypolicies --policy-file=deny-sa-keys.json
gcloud iam policies list --attachment-point=$ORG_AP --kind=denypolicies
gcloud iam policies get deny-sa-keys --attachment-point=$ORG_AP --kind=denypolicies --format=json > cur.json
# edit cur.json keeping "etag", then
gcloud iam policies update deny-sa-keys --attachment-point=$ORG_AP --kind=denypolicies --policy-file=cur.json
gcloud iam policies delete deny-sa-keys --attachment-point=$ORG_AP --kind=denypolicies
```

## Terraform
`google_iam_deny_policy` with `parent = urlencode("cloudresourcemanager.googleapis.com/organizations/${var.org_id}")`.

## Gotchas
- Principal syntax differs from allow policies: `principal://goog/subject/alice@example.com`,
  `principalSet://goog/group/<email>`, `principal://iam.googleapis.com/projects/-/serviceAccounts/<email>`, `principalSet://goog/public:all`.
- Grant `denyAdmin` to a small group.
- Access changes are eventually consistent; test in a sandbox folder first.

## Verify
- [ ] `gcloud iam policies list` shows the policy; a test principal gets denied with the deny policy in Policy Troubleshooter.

## Checked

- Date: 2026-10-27
- Confirmed against the deny-access and deny-overview pages (organisation/folder/project attachment points, URL-encoded `%2F` form, 500 policies and 500 rules per resource, `roles/iam.denyAdmin` and `roles/iam.denyReviewer`, principal formats for `principal://goog/subject/...`, `principalSet://goog/group/...`, `principalSet://goog/public:all`, service-account principal) and the gcloud `iam policies` group (create, delete, get, list, update with `--attachment-point`, `--kind`, `--policy-file`, `--etag`).
- Removed: "Org Admin does not include denyAdmin", the deny-rule-on-`denypolicies.*` self-protection tip and the "no dry-run" claim.

Method: documentation only; no commands were run.
