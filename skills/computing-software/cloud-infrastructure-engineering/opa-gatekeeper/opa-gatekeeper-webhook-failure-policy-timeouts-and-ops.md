---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-webhook-failure-policy-timeouts-and-ops
name: opa-gatekeeper-webhook-failure-policy-timeouts-and-ops
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, failure-policy, timeout, validatingwebhookconfiguration, delete, connect, admission]
level: advanced
status: docs-checked
description: "Tune the Gatekeeper ValidatingWebhookConfiguration: failure policy, timeouts, and adding DELETE and CONNECT operations, with the audit caveats."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/customize-admission.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper webhook failure policy timeouts and ops

Gatekeeper ships a `ValidatingWebhookConfiguration` named `gatekeeper-validating-webhook-configuration` with two webhooks: one checks requests against constraints; the other checks namespace labels so that permission to label a namespace cannot bypass all constraints.

Two settings matter most:
- Timeout: how long the API server waits. A timeout longer than the overall request timeout means the request times out before the failure policy applies.
- Failure policy: `Ignore` lets requests through if the webhook errors, times out, returns 5xx or is down; `Fail` rejects them. The constraint webhook defaults to `Ignore`, trading enforcement for availability. The namespace-label webhook defaults to `Fail`, since it is only called for namespace changes.

Validate deletes by adding `DELETE` to `operations` of the webhook; add `CONNECT` to review `kubectl exec`.

```yaml
operations:
  - CREATE
  - UPDATE
  - DELETE
```

Caveats for DELETE: a deleted object is gone, so non-compliant deletes cannot be found by audit, and with fail-open an imperfectly enforced policy cannot be repaired by audit. Fail closed to improve enforcement.

## Checked

Method: docs-checked 2026-11-09 against the Gatekeeper website docs customize-admission.md (raw markdown, read in full).
