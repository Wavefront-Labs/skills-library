---
id: computing-software.cloud-infrastructure-engineering.google-cloud.iam-policy-audit-and-role-grant-review
name: iam-policy-audit-and-role-grant-review
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam, iam-policy-audit, get-iam-policy, role-grant-review, access-review, search-all-iam-policies, effective-iam, iam-policy-export, external-members, allusers-audit, quarterly-access-review, iam-policy-version-3]
level: practitioner
status: docs-checked
description: "Run a repeatable IAM access review: export bindings with Cloud Asset search, find user, public and privileged grants, compute effective access, record sign-off."
sources: ["https://docs.cloud.google.com/asset-inventory/docs/searching-iam-policies", "https://docs.cloud.google.com/policy-intelligence/docs/analyze-iam-policies", "https://docs.cloud.google.com/iam/docs/policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM policy audit and role grant review

**Goal:** answer "who can do what, where" for an organisation with a repeatable script and keep a
record of the review.

## 1. Single resource
```bash
gcloud projects get-iam-policy <PROJECT_ID> --format=json
gcloud organizations get-iam-policy <ORG_ID> --format=json
gcloud iam service-accounts get-iam-policy <SA_EMAIL>
gcloud storage buckets get-iam-policy gs://<BUCKET>
```
Policies with conditions need policy version 3 to be read in full; keep `condition.expression`
in the review.

## 2. Organisation-wide export
Needs the Cloud Asset Viewer role (`roles/cloudasset.viewer`), which includes
`cloudasset.assets.searchAllIamPolicies` and `cloudasset.assets.analyzeIamPolicy`.
```bash
gcloud asset search-all-iam-policies --scope=organizations/<ORG_ID> --format=json
gcloud asset search-all-iam-policies --scope=organizations/<ORG_ID> --query='memberTypes:user'
gcloud asset search-all-iam-policies --scope=organizations/<ORG_ID> --query='memberTypes:(allUsers OR allAuthenticatedUsers)'
```
`memberTypes` accepts user, group, domain, serviceAccount, allUsers and allAuthenticatedUsers.
Export to BigQuery with `gcloud asset export --content-type=iam-policy` for history and joins.

## 3. Findings to look for
1. `user:` members where groups should be used (allow break-glass exceptions).
2. Members outside your domains and service accounts from other projects.
3. Basic roles (owner, editor, viewer) on projects.
4. `allUsers` / `allAuthenticatedUsers` bindings.
5. Roles that enable privilege escalation (service account token creator, service account user, key admin, IAM admin roles) granted broadly.

## 4. Effective access
```bash
gcloud asset analyze-iam-policy --organization=<ORG_ID> --identity='user:alice@example.com' \
  --expand-groups --expand-resources
```
`--expand-groups` expands groups into individual members (it needs the `groups.read` Google
Workspace permission, in the Groups Reader Admin role and stronger ones). `--expand-resources`
lists up to 1,000 relevant descendant resources of parent resources.

## 5. Review process
- Quarterly: run the export, diff it against the last one, send each owner a sheet with an explicit keep/remove decision per row, and archive the signed sheet with the date.
- Apply changes through your IAM-as-code workflow rather than by hand in the console.

## Gotchas
- Bindings of deleted principals show as `deleted:...` with a `?uid=` suffix for some types, such as service accounts.
- When you write back a policy that contains conditions, request and set version 3 and keep the etag, or conditions can be dropped (see the etag skill).

## Verify
- [ ] Org-wide export saved; counts of user, external, basic-role, public and escalation-role bindings reported.
- [ ] Each finding has an owner and a change or an accepted exception.

## Checked
2026-10-31. Confirmed against "Search IAM policies" (`memberTypes` values and query), "Analyze IAM policies" (`roles/cloudasset.viewer`, permissions, `--expand-groups`, `--expand-resources` 1,000 resources, groups.read) and the IAM policies page (deleted: prefix and ?uid=, version 3 and etag). gcloud flags were checked against the command reference. Removed: `policy:` query forms, the claim that get-iam-policy shows only direct bindings, supported-asset-type and eventual-consistency remarks, the `--condition-from-file` remark and the owner-conditions claim, `--output-resource-edges` and the permission-targeted example (not confirmed in fetched pages).
Method: documentation only; no commands were run.
