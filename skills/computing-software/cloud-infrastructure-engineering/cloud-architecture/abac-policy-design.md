---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.abac-policy-design
name: abac-policy-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, abac-policy-design, abac, attribute-based-access-control, session-tags, azure-abac-conditions, rbac-vs-abac]
level: advanced
status: docs-checked
description: "Choose RBAC vs ABAC and design attribute-based policies (AWS tags/session tags, Azure role assignment conditions, IAM conditions) that scale without role explosion."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://learn.microsoft.com/azure/role-based-access-control/conditions-overview", "https://docs.cloud.google.com/iam/docs/conditions-overview", "https://csrc.nist.gov/pubs/sp/800/162/upd2/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC vs ABAC authorisation models

## When ABAC helps
RBAC role count explodes when permissions depend on project/team/environment (role per project x
per environment). ABAC grants one policy: allow when principal attribute matches resource attribute.

## AWS
- Tag principals (IAM role tags, or **session tags** from the IdP via SAML/OIDC attributes).
- Policy conditions: `aws:PrincipalTag/project` equals `aws:ResourceTag/project`; require tags on
  create with `aws:RequestTag/project` and `aws:TagKeys`; prevent tag changes by non-admins.
- Not every service supports ABAC; check the "AWS services that work with IAM" list.

## Azure
- Role assignment **conditions** (ABAC) add a check on top of an RBAC role assignment. Today they apply to
  role assignments with blob or queue storage data actions, at the same scope as the assignment.
- Example: allow read only when the blob index tag `Project` equals the user's custom security
  attribute `Project`. Custom security attributes on a principal can be used in a condition.
- Conditions only filter down granted permissions; they cannot explicitly deny. They can reduce the
  number of role assignments, which are limited per subscription.

## Google Cloud
- IAM Conditions are expressions on variables such as `request.time` and `resource.name`; resource tags
  are usable in allow-policy bindings (`resource.matchTag(...)`) and, as the only attribute, in deny rules.

## Design steps
1. Choose a small, controlled attribute set (project, environment, data-classification).
2. Make attributes authoritative: set by IdP/HR or vending pipeline, not editable by users.
3. Enforce tagging on resource creation; deny tag modification except by automation.
4. Combine: RBAC for job function (what actions), ABAC for scope (which resources).
5. Test with negative tests (access that must be denied).

## Gotchas
- If users can edit their own or resource tags, ABAC is bypassable.
- Debugging denied requests is harder; log and document conditions.

## Verify
- [ ] Attempt cross-project access is denied in tests.
- [ ] Tag modification restricted to automation roles.

## Checked
2026-11-08. Confirmed against the AWS IAM ABAC page and condition-keys reference (PrincipalTag, ResourceTag,
RequestTag, TagKeys, session tags from SAML/OIDC), the Azure ABAC conditions overview (scope, blob/queue data
actions, custom security attributes, no explicit deny, role assignment limit) and the Google Cloud IAM conditions
overview (variables, matchTag, deny rules). Removed the unsourced policy-simulator advice. NIST SP 800-162 page
read for the ABAC definition only.
Method: documentation only; no commands were run.
