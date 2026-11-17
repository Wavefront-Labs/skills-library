---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gcp-iam-and-org-policy
name: gcp-iam-and-org-policy
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, org-policy, organization-policy-service, custom-constraints, cel, list-constraints, boolean-constraints, policy-inheritance, inheritfromparent, dry-run, policy-simulator, resource-manager-tags, conditional-org-policy, iam-deny-policies, deniedpermissions, exceptionprincipals, principal-access-boundary, iam-conditions, resource-matchtag, guardrails, policy-as-code, gcloud-org-policies]
level: advanced
status: docs-checked
description: "Author GCP guardrails: custom org policy constraints in CEL, list-policy inheritance, tag-conditional policies, dry-run, IAM deny policies and principal access boundaries."
sources: ["https://cloud.google.com/resource-manager/docs/organization-policy/understanding-hierarchy", "https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints", "https://cloud.google.com/resource-manager/docs/organization-policy/dry-run-policy", "https://cloud.google.com/iam/docs/deny-access", "https://cloud.google.com/iam/docs/principal-access-boundary-policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCP IAM and org policy — authoring guardrails that don't break production

**Goal:** preventive controls written as code, rolled out in dry-run, scoped by tags
where exceptions are needed, and backed by IAM deny and principal-access-boundary
policies that cap what any allow binding can do. Hierarchy, role binding and service
accounts are in
`computing-software.cloud-infrastructure-engineering.google-cloud.projects-iam-and-service-accounts`.

## 1. Understand how org policies combine
- Policies set at org, folder or project; the **effective policy** is computed down the tree.
- **List constraints** (e.g. `gcp.resourceLocations`, `compute.vmExternalIpAccess`): a child
  policy with `inheritFromParent: true` **merges** its values with the parent's; without it,
  the child **replaces** them.
- Deny values always take precedence during policy reconciliation (hierarchy-evaluation page).
- Check effective result: `gcloud org-policies describe <CONSTRAINT> --project=<PROJECT_ID> --effective`.

## 2. Write custom constraints
When no predefined constraint fits, write one against a resource type from the supported-services list:
```yaml
name: organizations/<ORG_ID>/customConstraints/custom.<CONSTRAINT_NAME>
resourceTypes: [<SERVICE>.googleapis.com/<RESOURCE_TYPE>]
methodTypes: [CREATE, UPDATE]
condition: "<CEL over the resource's API fields> == '<value>'"
actionType: DENY
displayName: <one-line description>
```
`methodTypes` accepts CREATE, UPDATE, DELETE, REMOVE_GRANT and GOVERN_TAGS; `actionType` is ALLOW or DENY (Organization Policy API v2).
`gcloud org-policies set-custom-constraint constraint.yaml`, then enforce it like any other
constraint with a policy file. Notes:
- `condition` is CEL over the resource's **API representation**; field names follow the REST
  resource (check them against the API reference, not the console).
- Prefer `DENY` constraints: they read as "forbid X" and compose predictably.

## 3. Roll out safely
1. Set the policy with a `dryRunSpec` alongside (or instead of) `spec`. Violations are logged
   to Cloud Audit Logs as dry-run denials without blocking.
2. Use **Policy Simulator for organization policies** (`gcloud policy-intelligence simulate orgpolicy`) to see which resources a change would affect.
3. Promote `dryRunSpec` to `spec` after a soak period with no unexpected hits.
Keep policy YAML in Git and apply with `gcloud org-policies set-policy` or Terraform
`google_org_policy_policy`.

## 4. Exceptions with tags, not project lists
Create a **Resource Manager tag** (e.g. `<ORG_ID>/allow-public-ip` with value `yes`), bind it
to the exceptional project/folder, and write a rule with a condition (confirm the `matchTag` syntax on the Organization Policy tags page before use):
```yaml
spec:
  rules:
  - condition: {expression: "resource.matchTag('<ORG_ID>/allow-public-ip', 'yes')"}
    enforce: false
  - enforce: true
```
Tag bindings are themselves IAM-controlled — restrict who can attach the exception tag, or the guardrail is self-service.

## 5. IAM deny policies
Deny policies attach to org, folder or project and override any allow:
```json
{"rules": [{"denyRule": {
  "deniedPrincipals": ["principalSet://goog/public:all"],
  "exceptionPrincipals": ["principalSet://goog/group/break-glass@example.com"],
  "deniedPermissions": ["iam.googleapis.com/roles.create", "iam.googleapis.com/serviceAccountKeys.create"]}}]}
```
`gcloud iam policies create no-key-creation --attachment-point=cloudresourcemanager.googleapis.com%2Forganizations%2F<ORG_ID> --kind=denypolicies --policy-file=deny.json`
(the attachment point is URL-encoded: `/` becomes `%2F`).
Permission names use the v2 form `iam.googleapis.com/roles.create`; only permissions
listed on the deny-supported-permissions page are accepted. Denial conditions can only use resource-tag functions.

## 6. Principal access boundary (PAB)
PAB policies limit which **resources** a set of principals can ever access (e.g. only
resources in your org), regardless of what they were granted — the defence against
grants into foreign projects and data exfiltration via credentials. Bind to principal sets
such as your workforce pool or org's identities. Newer feature; verify which services enforce it.

## Gotchas
- Setting a list policy at a folder without `inheritFromParent` silently discards the org's values.
- Org policies are not retroactive (existing public IPs, keys stay).
- Some constraints are enforced by default on newer organisations (for example `iam.automaticIamGrantsForDefaultServiceAccounts` for organisations created on or after 2024-05-03) — know which before assuming an open baseline.

## Verify
- [ ] All org policies and custom constraints are in Git; `gcloud org-policies list --organization=<ORG_ID>` matches.
- [ ] Every new enforcement ran in dry-run with Policy Simulator reviewed before promotion.
- [ ] Exceptions are tag-conditional, and `tagUser` on exception tags is restricted.
- [ ] A deny policy blocks SA key and custom-role creation except for break-glass; tested with a non-exempt principal.
- [ ] `--effective` checks on a sample project per folder show the intended merged list values.

## Checked

- Date: 2026-10-27
- Confirmed against the hierarchy-evaluation page (`inheritFromParent` merge, deny values win), the dry-run page (`dryRunSpec`), the Organization Policy API v2 `CustomConstraint` schema (`resourceTypes`, `methodTypes` enum, `condition`, `actionType`, `displayName`), the gcloud `org-policies` group (`set-custom-constraint`, `set-policy`, `describe --effective`, `list`), `policy-intelligence simulate orgpolicy`, the deny-access page (URL-encoded attachment point, `iam.googleapis.com/roles.create` form, tag-only denial conditions, `principalSet://goog/public:all`) and the constraints list.
- Fixed: the deny-policy command used an unencoded attachment point (needs `%2F`). Removed: Cloud Run custom-constraint example (resource type and field not confirmed), boolean-constraint precedence and `reset: true` claims, CREATE/UPDATE-only claim, `tagUser` role and tag-propagation claims.

Method: documentation only; no commands were run.
