---
id: computing-software.cloud-infrastructure-engineering.google-cloud.wif-attribute-mapping-and-conditions
name: wif-attribute-mapping-and-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workload-identity-federation, attribute-mapping, attribute-conditions, cel-attribute-mapping, google-subject, google-groups-mapping, principalset, assertion-claims, workload-identity-provider-design, claim-extraction]
level: advanced
status: docs-checked
description: "Design Workload Identity Federation attribute mappings and CEL conditions: a stable google.subject, derived attributes, allowlist conditions, principalSet forms."
sources: ["https://docs.cloud.google.com/iam/docs/workload-identity-federation", "https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines", "https://github.com/google/cel-spec"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WIF attribute mapping and conditions

**Goal:** provider configs that admit exactly the workloads you intend and expose exactly the
attributes you grant on, written once and readable in a review.

## 1. The two expressions
- **Attribute mapping**: `TARGET_ATTRIBUTE=SOURCE_EXPRESSION`, where the source is a CEL expression over the external token's attributes (claims), reached through the `assertion` map.
- **Attribute condition**: a CEL expression over `assertion` and the mapped attributes. If it is true the credential is accepted; otherwise it is rejected.

## 2. Targets
| Target | Rule | Used by |
|---|---|---|
| `google.subject` | required; unique; at most 127 characters | `principal://` bindings and Cloud Logging |
| `google.groups` | optional set of groups | `principalSet://.../group/GROUP_ID` |
| `attribute.NAME` | optional; up to 50 custom attributes | `principalSet://.../attribute.ATTRIBUTE_NAME/ATTRIBUTE_VALUE` |

Full identifiers are `principal://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/subject/<value>`
and the `principalSet://` forms above on the same prefix. Use the project number, not the project ID.
For OIDC and SAML you must supply the mappings. AWS has a default (`google.subject=assertion.arn` plus
an `attribute.aws_role` that strips the session name); X.509 maps `google.subject` to `assertion.subject.dn.cn`.

## 3. CEL from the documentation
```text
google.subject=assertion.sub
google.subject='myprovider::' + assertion.aud + '::' + assertion.sub
attribute.environment=assertion.arn.contains(":instance-profile/Production") ? "prod" : "test"
attribute.aws_role=assertion.arn.contains('assumed-role') ? assertion.arn.extract('{account_arn}assumed-role/') + 'assumed-role/' + assertion.arn.extract('assumed-role/{role_name}/') : assertion.arn
attribute.username=assertion.email.split("@")[0]
attribute.department=assertion.department.join(".")
```
Map literals can translate IDs to names (`{"<guid>": "Workload1"}[assertion.workload_id]`).

## 4. Conditions as an allowlist
```text
attribute.aws_role == "ROLE_MAPPING"
assertion.repository_owner=='ORGANIZATION' && assertion.ref=='refs/heads/main'
```
Use a condition to restrict which identities may use the pool, and to stop credentials meant for
another platform being used with Google Cloud (the confused deputy problem). For GitHub, map at least
`google.subject=assertion.sub`, and pin `assertion.repository_owner`.

## 5. Patterns
- Google recommends one pool per non-Google Cloud environment (development, staging, production).
- Avoid granting to every identity in a pool; limit by attributes and conditions.
- Grant either directly on the resource with `principal://`/`principalSet://`, or through service account impersonation, which requires `roles/iam.workloadIdentityUser` on the service account.
- Treat a mapping edit as a security change; keep it in version control.

## Verify
- [ ] A decoded sample token for each issuer is saved beside the provider config and every mapping line resolves against it.
- [ ] A token that violates the condition is rejected (test with a different repo, account or tenant).

## Checked
2026-10-31. Confirmed against "Workload Identity Federation" (mapping format, targets, 127 characters, 50 custom attributes, CEL examples, defaults, conditions, principal identifier forms, pool-per-environment, impersonation role) and the deployment-pipelines page (GitHub subject mapping and `repository_owner` conditions). Removed: ~4096/2048 character limits, error message strings, Terraform resource name, workforce-only targets, SAML/AWS claim gotchas, `has()`/`matches` function claims, Azure/Kubernetes example conditions and the audit-log field name (not confirmed in fetched pages).
Method: documentation only; no commands were run.
