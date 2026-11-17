---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-vap-operations-intersection-and-delete
name: opa-gatekeeper-vap-operations-intersection-and-delete
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, vap, operations, delete, intersection, targets-operations, webhook]
level: advanced
status: docs-checked
description: "Control which operations generated ValidatingAdmissionPolicies cover by intersecting ConstraintTemplate targets.operations with the webhook operations."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/validating-admission-policy.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper vap operations intersection and delete

The `operations` of a generated VAP are the intersection of:
1. operations on Gatekeeper validating webhook (default CREATE and UPDATE, optionally DELETE), and
2. the optional `targets[].operations` field in the ConstraintTemplate.

If `targets[].operations` is omitted, the VAP simply inherits the webhook operations with no filtering.

Consequences:
- A template that lists `DELETE` yields a VAP with `DELETE` only if the webhook also handles DELETE.
- Partial overlap (template CREATE and DELETE, webhook CREATE and UPDATE) still generates the VAP with the intersection (CREATE), and logs a non-fatal warning. In per-constraint mode the warning appears in the `vap.k8s.io` entry under ConstraintPodStatus `status.enforcementPointsStatus`.
- No overlap (template only DELETE, webhook CREATE and UPDATE) means the VAP is not generated.

To enable DELETE for VAP policies, first enable delete operations on the webhook (Helm value, or by adding DELETE to the ValidatingWebhookConfiguration operations as described in the admission customisation guide), then list `DELETE` in the template.

## Checked

2026-11-08: read the Configuring VAP Operations section and the constraint-mode warning note of website/docs/validating-admission-policy.md, and the DELETE section of website/docs/customize-admission.md in the Gatekeeper repo (partial reads). Confirmed the intersection rule, overlap cases, the Helm value and the webhook configuration route. Removed: the claim that deleted objects cannot be audited, which was not read in the cited page.

Method: documentation only; no commands were run.
