---
id: computing-software.messaging-and-integration.apache-camel.enrich
name: enrich
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, enrich, content-enricher, aggregation-strategy]
level: practitioner
status: docs-checked
description: "Camel Enrich EIP: producer-based content enrichment, aggregationStrategy argument order, aggregateOnException, variableReceive, dynamic URIs and option defaults."
sources:
  - https://camel.apache.org/components/next/eips/enrich-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enrich

Fetches data from a resource endpoint with a Producer (request-reply, e.g. a web service) and merges it into the exchange. For event-style sources such as files use Poll Enrich.

Default: with no aggregation strategy the reply replaces the body, like `to`. With `variableReceive` the reply body goes into a variable and the message body and headers stay unchanged.

Options (defaults):
- `expression` (required) computes the endpoint URI
- `aggregationStrategy`: first parameter is the original exchange, second is the resource exchange
- `aggregationStrategyMethodName`, `aggregationStrategyMethodAllowNull`
- `aggregateOnException` false (aggregation skipped if retrieval throws)
- `shareUnitOfWork` false
- `cacheSize` (0 default, -1 off)
- `ignoreInvalidEndpoint` false
- `allowOptimisedComponents` true, `autoStartComponents` true
- `variableSend`, `variableReceive`
- `allowedSchemes` unset

Property: `CamelToEndpoint`.

```java
from("direct:start").enrich("http:remoteserver/foo", aggregationStrategy).to("mock:result");
.enrich().simple("http:myserver/${header.orderId}/order")
.enrich().constant("jms:queue:stock").variableReceive("stock")
```

`AggregationStrategies.string(":")` is a built-in strategy that joins with a colon.

Verify: with `variableReceive("stock")` the body is unchanged and `${variable.stock}` holds the reply.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Enrich EIP page: option list and defaults (aggregateOnException false, shareUnitOfWork false, ignoreInvalidEndpoint false, allowOptimisedComponents true, autoStartComponents true, cacheSize 0 or -1, allowedSchemes unset), default reply-replaces-body behaviour, variableReceive and variableSend semantics, aggregate parameter order as the page words it, CamelToEndpoint, dynamic URI example and AggregationStrategies.string(":") all match. No commands were run.
