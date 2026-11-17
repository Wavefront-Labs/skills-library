---
id: computing-software.messaging-and-integration.apache-camel.recipient-list
name: recipient-list
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, recipient-list, dynamic-routing, parallel-processing]
level: practitioner
status: docs-checked
description: "Camel Recipient List EIP: expression-driven endpoints, delimiter, parallelProcessing, stopOnException, ignoreInvalidEndpoints, timeout, allowedSchemes and output body rules."
sources:
  - https://camel.apache.org/components/next/eips/recipientList-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recipient List

The required expression returns endpoint URIs (comma string, Collection or Iterator); the same message goes to each.

Options (defaults):
- `delimiter` `,` (`false` turns splitting off)
- `parallelProcessing` false (caller still waits)
- `stopOnException` false
- `ignoreInvalidEndpoints` false (skipped URIs logged at DEBUG)
- `streaming` false (true = reply order)
- `cacheSize` (0 default size, -1 off)
- `onPrepare` processor, e.g. deep clone
- `timeout` 0 ms, with parallel processing
- `synchronous` false
- `allowedSchemes` e.g. `http,https`; unset allows any

```java
from("jms:queue:a").recipientList(constant("seda:x,seda:y,seda:z"));
from("direct:a").recipientList(header("myHeader"), ";");
from("direct:a").recipientList(header("myHeader")).parallelProcessing();
```

With header `"activemq:queue:foo;activemq:topic:hello ; log:bar"` and delimiter `;` you get three endpoints; spaces are trimmed.

Without an aggregation strategy the output body is the last recipient's reply. The EIP does not change the exchange pattern; use `setExchangePattern`, or per-endpoint `?exchangePattern=InOut`.

Verify: by default the remaining recipients are still processed when one fails; with `stopOnException` further processing stops and the exception is thrown to the error handler.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Recipient List EIP page: expression result types, delimiter default and false, parallelProcessing, synchronous, timeout 0, stopOnException, ignoreInvalidEndpoints with DEBUG logging, streaming, cacheSize, onPrepare, allowedSchemes, last-recipient output body, exchange pattern note and the semicolon header example with trimming all match. The old verify line named a specific third recipient; it was reworded to the documented behaviour. No commands were run.
