---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-iam-deny-policy-denials
name: troubleshooting-iam-deny-policy-denials
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam, deny-policies, deny-troubleshooting, deny-policy-audit, policy-troubleshooter, permission-denied]
level: advanced
status: docs-checked
description: "Work out whether a PERMISSION_DENIED comes from a deny policy, find the policy and rule on any ancestor, test with Policy Troubleshooter and audit deny policies org-wide."
sources: ["https://cloud.google.com/iam/docs/troubleshoot-policies", "https://cloud.google.com/iam/docs/deny-access", "https://cloud.google.com/sdk/gcloud/reference/iam/policies/list", "https://cloud.google.com/sdk/gcloud/reference/policy-intelligence/troubleshoot-policy/iam"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting deny-policy denials

IAM always checks relevant deny policies before allow policies, so a deny rule on the resource or any ancestor wins over
the roles a principal was granted. The API error looks the same as "no role", so check deny explicitly.

## 1. Run the troubleshooter first
```bash
gcloud policy-intelligence troubleshoot-policy iam \
  //cloudresourcemanager.googleapis.com/projects/<P> \
  --principal-email=alice@example.com --permission=resourcemanager.projects.delete
```
Read `overallAccessState`, then `denyPolicyExplanation` (which deny policy/rule matched) and the allow-policy explanation. Console: the
Policy Troubleshooter page shows the same. The gcloud reference describes this command as troubleshooting allow and deny policies.

## 2. List deny policies on every ancestor
The attachment point is URL-encoded (`/` becomes `%2F`):
```bash
gcloud iam policies list --attachment-point=cloudresourcemanager.googleapis.com%2Forganizations%2F<ORG_ID> --kind=denypolicies
gcloud iam policies list --attachment-point=cloudresourcemanager.googleapis.com%2Ffolders%2F<FOLDER_ID> --kind=denypolicies
gcloud iam policies list --attachment-point=cloudresourcemanager.googleapis.com%2Fprojects%2F<PROJECT_ID> --kind=denypolicies
gcloud iam policies get <POLICY_ID> --attachment-point=<ENCODED_ATTACHMENT_POINT> --kind=denypolicies --format=json
```
Each rule has `deniedPrincipals`, `exceptionPrincipals`, `deniedPermissions` (v2 form
`iam.googleapis.com/roles.create`), `exceptionPermissions` and an optional
`denialCondition` (which can only use resource-tag functions).

## 3. Common causes
- A broad `principalSet://goog/public:all` deny with the caller not in `exceptionPrincipals`.
- A tag on the resource (or inherited) satisfying `resource.matchTag(...)` in the denial condition.
- Group membership: denied principal is a group the caller is in.

## 4. Audit org-wide
Viewing deny policies needs `roles/iam.denyReviewer` (view) or `roles/iam.denyAdmin` (view and manage) on the organisation. Keep deny policies in source control and alert on changes to them in the Admin Activity audit logs.

## Gotchas
- Each resource can have up to 500 deny policies and 500 deny rules across them; consolidate rather than add one per incident.
- Not every permission is deny-able; check the deny-supported-permissions page.
- Access changes are eventually consistent; test after a short wait.

## Verify
- [ ] Troubleshooter output names the exact policy and rule for a known denial.
- [ ] Every deny policy is in source control.

## Checked

- Date: 2026-10-27
- Confirmed against the IAM deny-access and deny-overview pages (deny checked before allow, URL-encoded attachment point, 500 policies and 500 rules per resource, `exceptionPermissions`, `denialCondition` limited to tag functions, `denyReviewer` and `denyAdmin`, v2 permission form `iam.googleapis.com/roles.create`, eventual consistency), the troubleshooting-access page (`overallAccessState`, `denyPolicyExplanation`), and gcloud references for `iam policies list/get` and `policy-intelligence troubleshoot-policy iam` (`--principal-email`, `--permission`).
- Removed: the "PAB then deny then allow" order claim, v1-form permission claim, Terraform resource name and the audit method names. Replaced the `sed` loop with literal encoded attachment points.

Method: documentation only; no commands were run.
