---
id: computing-software.cloud-infrastructure-engineering.istio.istio-fault-injection
name: istio-fault-injection
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, fault-injection, delay-fault, abort-fault]
level: practitioner
status: docs-checked
description: "Add HTTP delay and abort faults scoped to a test header with a VirtualService, to test timeout and retry behaviour without changing code."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/fault-injection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Faults are configured per route in a VirtualService, scoped by a match so only test traffic is affected.

```yaml
http:
- match: [{headers: {end-user: {exact: tester}}}]
  fault:
    delay: {percentage: {value: 100}, fixedDelay: 7s}
  route: [{destination: {host: ratings, subset: v1}}]
- route: [{destination: {host: ratings, subset: v1}}]
```

For an abort fault use `fault.abort` with `httpStatus: 500` and a `percentage.value: 100` (the Istio task's example).

Gotchas: a delay can expose mismatched timeouts upstream. In the Bookinfo task the 7 s delay did not trip the reviews-to-ratings 10 s timeout, but the productpage-to-reviews call (3 s plus 1 retry) failed after about 6 s, so the failure showed up somewhere other than where the fault was injected. Faults apply only to requests matching the rule; other users see nothing (in the task, everyone but the test user is routed to reviews:v1).

## Checked

2026-11-03. Confirmed against the Istio Fault Injection task: delay and abort VirtualService shapes (`fixedDelay: 7s`, `percentage.value: 100`, `abort.httpStatus: 500`), match on the `end-user` header, and the 6 s (3 s + 1 retry) timeout explanation. Removed: the invented curl verify step, the unsourced remarks on low percentages, fault/retry interaction and cleanup.
Method: documentation only; no commands were run.
