---
id: computing-software.cloud-infrastructure-engineering.google-cloud.vpc-sc-scoped-access-policies-for-delegated-admin
name: vpc-sc-scoped-access-policies-for-delegated-admin
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc-service-controls, scoped-access-policies, access-context-manager, delegated-administration, policy-scopes]
level: practitioner
status: docs-checked
description: "Delegate VPC Service Controls administration with scoped access policies on folders or projects: create the policy, grant scoped admins, and the title and scope rules."
sources: ["https://docs.cloud.google.com/access-context-manager/docs/create-access-policy", "https://docs.cloud.google.com/sdk/gcloud/reference/access-context-manager/policies/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC-SC scoped access policies for delegated administration

An organization has one organization-level access policy and can have many scoped policies. A **scoped policy** is an additional access policy whose scope is one folder
or project, so a team can manage perimeters for its own projects.

## Create
```bash
gcloud access-context-manager policies create --organization=<ORG_ID> \
  --scopes=folders/<FOLDER_ID> --title=payments_team_policy
gcloud access-context-manager policies list --organization=<ORG_ID>
# delegate
gcloud access-context-manager policies add-iam-policy-binding <SCOPED_POLICY_ID> \
  --member=group:payments-secops@example.com --role=<ROLE>   # full predefined role path, e.g. roles/accesscontextmanager.policyReader (the docs example)
```
The title is at most 50 characters, starts with a letter, and uses only ASCII letters, digits and underscores; it is case sensitive and unique within the organization. An organization-level policy must exist or scoped policies do not operate. Only VPC Service Controls supports scoped policies (keep org-level policies for services such as IAP).
The team then creates perimeters/access levels under `accessPolicies/<SCOPED_POLICY_ID>` that can only
include projects within the scope.

## Rules
- At most one folder or project as the scope of a scoped policy, and the scope must exist within the organization. Omit `--scopes` and the policy applies to the whole organization.

## Operations
Use the same commands with `--policy=<SCOPED_POLICY_ID>`:
```bash
gcloud access-context-manager perimeters create payments --policy=<SCOPED_POLICY_ID> \
  --title=payments --resources=projects/<PN1>,projects/<PN2> \
  --restricted-services=storage.googleapis.com,bigquery.googleapis.com --perimeter-type=regular
```

## Gotchas
- Central security should still monitor violations across all policies.

## Verify
- [ ] Team admin can create a perimeter in the scoped policy but gets PERMISSION_DENIED on the org policy.

## Checked
2026-10-31. Confirmed against the Access Context Manager "Create an access policy" page and the `gcloud access-context-manager policies create` reference: `--scopes` takes one folder or project, title rules, scoped policy needs an org-level policy, only VPC-SC supports scoped policies, add-iam-policy-binding usage. Removed: perimeter-overlap, bridge and access-level-sharing rules and the project-move gotcha (the scoped-policies page 404s; unconfirmed), and the `policyAdmin` role (not named in the docs). Commands checked with check_commands.py.
Method: documentation only; no commands were run.
