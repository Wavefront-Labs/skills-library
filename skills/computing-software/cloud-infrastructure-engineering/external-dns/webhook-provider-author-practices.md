---
id: computing-software.cloud-infrastructure-engineering.external-dns.webhook-provider-author-practices
name: webhook-provider-author-practices
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, webhook-status-codes, connection-reuse, webhook-timeouts, webhook-provider-authors]
level: sme
status: docs-checked
description: "Best practices for writing an ExternalDNS webhook provider: status codes that control retries, response body sizing, timeouts, cancellation and goroutine hygiene."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/webhook-provider.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a webhook provider well

**Status codes decide retry behaviour**

| Situation | Code | Effect |
|---|---|---|
| Records or AdjustEndpoints success | 200 | Accepted |
| ApplyChanges success | 204 | Accepted |
| Transient (rate limit, upstream timeout) | 5xx | Retried |
| Permanent (bad request, auth failure) | 4xx | Not retried, logged as failure |
| Redirect | 3xx | Permanent failure; do not use |

**Bodies and connection reuse**
- Always write a complete body, even on errors; `{}` or plain text is fine.
- Keep error bodies well under 1 MiB. ExternalDNS drains up to 1 MiB so the TCP connection returns to the pool; larger bodies discard the connection.
- Keep success bodies under the limit (32 MiB default). Beyond it decoding stops and the request fails.
- Do not stream indefinitely; finish and close.

**Timeouts and cancellation**
- Request context is propagated; shutdown or timeout cancels the in-flight connection.
- Handle abrupt drops: do not roll back partly applied changes without checking actual state first.
- Respond inside the read plus write timeout. Give long DNS API calls an internal timeout shorter than that.

**Hygiene**
- Close request bodies after reading to avoid goroutine leaks.
- Do not hold decoded `plan.Changes` or endpoint slices longer than needed; large zones make them big.

Running the provider as a localhost sidecar in the ExternalDNS pod is the layout the docs recommend.

## Checked

2026-11-04. Read the webhook provider tutorial (Best practices for webhook provider authors: status codes, response bodies and connection reuse, timeouts and cancellation, hygiene). Confirmed the status code table, the 1 MiB drain cap, the 32 MiB default and the context-propagation advice. Removed the word tested from the sidecar remark, which the page does not claim.

Method: documentation only; no commands were run.
