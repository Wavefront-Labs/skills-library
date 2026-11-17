---
id: computing-software.messaging-and-integration.apache-camel.wire-tap
name: wire-tap
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, wire-tap, async, onprepare]
level: practitioner
status: docs-checked
description: "Camel Wire Tap EIP: fire-and-forget InOnly copy on a separate thread, copy and dynamicUri defaults, onPrepare deep clone, thread pool exhaustion and stream caching."
sources:
  - https://camel.apache.org/components/next/eips/wireTap-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wire Tap

Sends a copy of each message to another endpoint while the original continues.

Options (defaults):
- `uri` required, can be Simple
- `copy` true
- `dynamicUri` true
- `onPrepare` (deep clone or custom logic)
- `executorService`
- `cacheSize` (0 default, -1 off)
- `ignoreInvalidEndpoint` false
- `allowOptimisedComponents` true, `autoStartComponents` true
- `allowedSchemes` unset
- `variableSend`, `variableReceive`
- `disabled` false

Behaviour:
- The tapped exchange is `InOnly` (fire and forget) on a separate thread, in parallel with the route.
- Only the Exchange is copied, not deep-cloned, so objects may be shared; use `onPrepare` to deep clone.
- Property `CamelToEndpoint`; body unchanged on output.
- When the default pool is exhausted, the calling thread runs further taps synchronously. Configure an explicit pool with a different rejection policy, bigger queue or more threads to avoid that.
- For stream bodies enable stream caching.

Examples: `direct:start` taps to `direct:tap` (which delays one second), so `log:result` can finish before `log:tap`. Dynamic: `jms:queue:backup-${header.id}`.

Verify: in the page's example the tap route delays one second, so `log:result` is logged before `log:tap`, showing the tap runs independently of the main route.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Wire Tap EIP page: option list and defaults (copy true, dynamicUri true, cacheSize 0 or -1, ignoreInvalidEndpoint false, allowOptimisedComponents true, autoStartComponents true, allowedSchemes unset, disabled false), InOnly separate-thread behaviour, shallow copy and onPrepare, CamelToEndpoint, thread pool exhaustion wording, stream caching advice and both examples match. No commands were run.
