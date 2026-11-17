---
id: computing-software.messaging-and-integration.apache-camel.routing-slip
name: routing-slip
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, routing-slip, pipeline, dynamic-routing]
level: practitioner
status: docs-checked
description: "Camel Routing Slip EIP: slip computed once, uriDelimiter, ignoreInvalidEndpoints, cacheSize, allowedSchemes and CamelSlipEndpoint."
sources:
  - https://camel.apache.org/components/next/eips/routingSlip-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Routing Slip

Routes a message through a list of endpoints in pipeline order, chosen per message at runtime.

Options:
- `expression` (required): String, Collection, Iterator/Iterable or array of URIs.
- `uriDelimiter` `,` for string results.
- `ignoreInvalidEndpoints` false (when true, invalid URIs are skipped, reason logged at DEBUG).
- `cacheSize` 1000 (`-1` off).
- `allowedSchemes` e.g. `http,https`; unset allows any.
- `disabled` false.

```java
from("activemq:cheese").routingSlip(header("whereTo"));
```

The slip is computed once before routing starts. If the next hop depends on each step's result, use Dynamic Router instead. An empty slip routes nowhere.

With header `direct:foo,xxx:bar` and `ignoreInvalidEndpoints`, `direct:foo` runs and `xxx:bar` is skipped.

Properties set: `CamelSlipEndpoint` (current slip endpoint) and `CamelToEndpoint` (where the exchange is being sent). The output body depends on the last endpoint.

Verify: a header listing `direct:a,direct:b` visits a then b, in order.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Routing Slip EIP page source (routingSlip-eip.adoc) and the Routing Slip model definition (routingSlip.json) from the apache/camel repository, which generate the cited page. Confirmed the expression result types, uriDelimiter default comma, ignoreInvalidEndpoints default false with DEBUG logging, cacheSize 1000 and -1, allowedSchemes, disabled, empty slip, compute-once behaviour versus Dynamic Router, CamelSlipEndpoint and CamelToEndpoint, and unknown output body. Nothing was removed. No commands were run.
