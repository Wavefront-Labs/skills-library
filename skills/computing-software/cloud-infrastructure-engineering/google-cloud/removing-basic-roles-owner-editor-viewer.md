---
id: computing-software.cloud-infrastructure-engineering.google-cloud.removing-basic-roles-owner-editor-viewer
name: removing-basic-roles-owner-editor-viewer
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam, basic-roles, primitive-roles, roles-editor, roles-owner, least-privilege, default-compute-service-account-editor, automaticiamgrantsfordefaultserviceaccounts, role-replacement, iam-recommender, owner-invitation]
level: practitioner
status: docs-checked
description: "Get Owner/Editor/Viewer off every project: stop the default SA Editor grant via org policy, replace basic roles using recommender data and keep a controlled Owner path."
sources: ["https://docs.cloud.google.com/iam/docs/best-practices-service-accounts", "https://docs.cloud.google.com/organization-policy/restrict-service-accounts", "https://docs.cloud.google.com/policy-intelligence/docs/role-recommendations-overview", "https://docs.cloud.google.com/asset-inventory/docs/search-allow-policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing basic roles (Owner, Editor, Viewer)

**Goal:** no human or service account holds `roles/editor` or `roles/owner` on a production
project, without breaking the pipeline or VM that silently relied on it.

## 1. Why these three are special
Basic roles are broad: Editor includes more than 3,000 permissions (including `iam.serviceAccountKeys.create`, so an Editor can mint service account keys). Some services create default service accounts when their API is first enabled, and depending on organisation policy those accounts are automatically granted Editor on the project. Google notes the grant is for convenience and is not needed: services use service agents, not default service accounts, to reach your resources.

## 2. Stop the bleeding first (org policy)
Enable the `constraints/iam.automaticIamGrantsForDefaultServiceAccounts` constraint (Disable Automatic IAM Grants for Default Service Accounts) on the organisation or a folder. It is enforced by default for organisations created on or after 3 May 2024. A policy file has this shape (the same pattern the docs show for other legacy managed constraints):
```yaml
name: organizations/<ORG_ID>/policies/iam.automaticIamGrantsForDefaultServiceAccounts
spec:
  rules:
  - enforce: true
```
```bash
gcloud org-policies set-policy policy.yaml
```
Default service accounts in new projects then have no access until you grant roles. Existing default service accounts keep Editor, so fix them in step 4.

## 3. Find every basic-role binding
```bash
gcloud asset search-all-iam-policies --scope=organizations/<ORG_ID> \
  --query="roles:roles/editor" \
  --flatten="policy.bindings[].members[]" \
  --format="table(resource, policy.bindings.role, policy.bindings.members)"
```
Repeat with `roles:roles/owner` and `roles:roles/viewer`. Sort results into humans (should become a group plus granular roles), the default compute service account, pipeline service accounts, and Google-managed service agents (leave those; they carry service-agent roles, not basic roles).

## 4. Replace, don't just remove
For each principal, learn what it actually used:
- **IAM recommender** (`gcloud recommender recommendations list --recommender=google.iam.policy.Recommender --location=global --project=<P>`): it compares granted permissions with those used in the last 90 days (the maximum observation period; the minimum defaults to 90 days and can be set to 30 or 60) and can recommend revoking Editor and replacing it with narrower roles.
- Or audit logs: filter `protoPayload.authenticationInfo.principalEmail="<SA>"` and group by `protoPayload.methodName` over a long window.
Then, with roles chosen from the recommendation:
```bash
gcloud projects add-iam-policy-binding <P> --member=serviceAccount:<SA> --role=<NARROW_ROLE>
gcloud projects remove-iam-policy-binding <P> --member=serviceAccount:<SA> --role=roles/editor
```
Better: a dedicated service account per workload (`--service-account` at VM create) and grant the default service account nothing.

Do removals project by project with a rollback note, in business hours, after checking logs for `PERMISSION_DENIED`.

## 5. Owner: the controlled path
Keep `roles/owner` only on a small admin group, or not at all; grant narrower admin roles at folder level instead. Review new `roles/owner` bindings through audit logs or Cloud Asset search.

## Gotchas
- The recommender looks back at most 90 days, so a yearly batch job's permissions will not appear; check its audit logs explicitly.
- Service agents need their own service-agent roles; never strip those, and never grant a service-agent role to anything but the agent.
- Some product consoles still suggest Editor for one-click setups; use the product's documented role list instead.

## Verify
- [ ] The search above returns zero `roles/editor` and `roles/owner` rows in production folders.
- [ ] The default-grants constraint is enforced at the organisation.
- [ ] After removal, no new `PERMISSION_DENIED` for the affected service accounts in Logs Explorer.

## Checked
2026-10-28. Confirmed against the IAM service account best-practices page (automatic Editor grant, constraint name, new-org default, existing accounts keep Editor, `serviceAccountKeys.create` in Editor), the role recommendations overview (90-day window, 30/60-day minimum option, Editor replacement example, "more than 3,000 permissions", `google.iam.policy.Recommender`), the organization policy service-account page (constraint and policy YAML pattern) and the Cloud Asset search pages (`roles:` query, flatten/format). Removed: the Owner/billing description, the claim about conditions, App Engine and GKE node role lists, Dataflow scaling note, the Viewer-and-secrets claim, owner invitation behaviour, the `iam.allowedPolicyMemberDomains` claim and fixed group names.
Method: documentation only; no commands were run.
