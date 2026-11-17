---
id: computing-software.messaging-and-integration.apache-camel.multicast
name: multicast
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, multicast, parallel-processing, onprepare]
level: practitioner
status: docs-checked
description: "Camel Multicast EIP: options and defaults, CamelMulticastIndex and Complete properties, and the shallow-copy trap fixed with onPrepare."
sources:
  - https://camel.apache.org/components/next/eips/multicast-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multicast

Copies the exchange and sends one copy to each output.

Options (defaults):
- `parallelProcessing` false (caller still waits)
- `synchronous` false (keep original thread for routing afterwards)
- `streaming` false (true = order replies return)
- `stopOnException` false (continues after a failure)
- `timeout` 0 ms, parallel only
- `shareUnitOfWork` false
- `aggregationStrategy` none (without it the last reply is used)
- `aggregationStrategyMethodAllowNull` false
- `parallelAggregate` false (deprecated)
- `executorService` (implies parallel)
- `onPrepare`
- `disabled` false

Properties: `CamelMulticastIndex` (from 0), `CamelMulticastComplete` (last copy), `CamelToEndpoint`.

Copy behaviour: the copy is shallow. Mutable bodies are shared, so a change in one branch shows up in others. Use `onPrepare` with a processor that deep-copies the body.

Verify: mutate a mutable body in one output; the change is visible in the other outputs unless `onPrepare` deep-copies it.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Multicast EIP page source (multicast-eip.adoc) and the Multicast model definition (multicast.json) from the apache/camel repository, which generate the cited page. Confirmed every option and default listed (parallelProcessing, synchronous, streaming, stopOnException, timeout 0, shareUnitOfWork, aggregationStrategy last reply default, aggregationStrategyMethodAllowNull, deprecated parallelAggregate, executorService implying parallel, onPrepare, disabled), the CamelMulticastIndex, CamelMulticastComplete and CamelToEndpoint properties, and the shallow copy note. Replaced the StringBuilder verify step, which the page does not describe, with the page's statement. No commands were run.
