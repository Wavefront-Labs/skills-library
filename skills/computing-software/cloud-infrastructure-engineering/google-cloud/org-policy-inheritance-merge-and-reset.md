---
id: computing-software.cloud-infrastructure-engineering.google-cloud.org-policy-inheritance-merge-and-reset
name: org-policy-inheritance-merge-and-reset
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, org-policy, org-policy-inheritance, inherit-from-parent, reset-policy, policy-evaluation, list-constraints-merge]
level: practitioner
status: docs-checked
description: "Predict how organization policies inherit and merge down the hierarchy: inheritFromParent for list constraints, reset to Google default, boolean overrides, and deletion behaviour."
sources: ["https://cloud.google.com/resource-manager/docs/organization-policy/understanding-hierarchy", "https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-policies", "https://cloud.google.com/sdk/gcloud/reference/org-policies/reset"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Org policy inheritance, merge and reset

## Rules
- No policy on a node = inherit the parent's effective policy.
- **Boolean** constraints: a child policy overrides (enforce or not); no merge.
- **List** constraints: child policy with `inheritFromParent: true` **merges** its values with the
  parent's effective values (allowed lists union, denied lists union; deny wins over allow for
  the same value). Without it, the child **replaces** the parent.
- `reset: true` sets the node to the constraint's Google default, ignoring parents.
- Deleting a policy (`gcloud org-policies delete`) returns to inheritance.

## Examples
```yaml
# folders/<DEV>: add one more allowed value on top of the org list
name: folders/<DEV>/policies/<LIST_CONSTRAINT>
spec:
  inheritFromParent: true
  rules:
  - values: {allowedValues: ["<ADDITIONAL_LOCATION>"]}
```
```yaml
# projects/<SANDBOX>: no inheritFromParent, so this replaces the parent's policy
name: projects/<SANDBOX>/policies/<LIST_CONSTRAINT>
spec:
  rules:
  - values: {allowedValues: ["<VALUE>"]}
```
```bash
gcloud org-policies reset <CONSTRAINT> --project=<P>       # back to Google default
gcloud org-policies delete <CONSTRAINT> --project=<P>      # back to inheriting
gcloud org-policies describe <CONSTRAINT> --project=<P> --effective
```

## Gotchas
- Deny values always take precedence during reconciliation of merged list policies.
- Check the constraint's own page for whether it is a list, boolean or managed constraint before predicting merge behaviour.
- `describe --effective` shows the resulting policy.

## Verify
- [ ] `describe --effective` on a leaf project matches your intended merged list.

## Checked

2026-10-28. Confirmed against: organization policy hierarchy page (inheritFromParent merges list values, deny values take precedence, reset to default policy) and gcloud org-policies reset/delete/describe flags via check_commands.

Removed or rewritten: allowAll/denyAll combination rules, in:/under: value-group expansion, managed-constraint behaviour, the claim about existing resources, and the specific constraint names and location groups in examples (replaced by placeholders).

Method: documentation only; no commands were run.
