---
id: computing-software.software-engineering.software-architecture.api-composition-for-cross-service-queries
name: api-composition-for-cross-service-queries
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, microservices, api-composition, query-patterns, aggregator, fan-out]
level: practitioner
status: verified
description: "Answer queries spanning several services with API composition: a composer that fans out in parallel, joins in memory, handles partial failure, and when to switch to CQRS."
sources: ["https://microservices.io/patterns/data/api-composition.html", "https://microservices.io/patterns/data/cqrs.html", "https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API composition for cross-service queries

**Pattern:** an API composer (BFF, gateway aggregation, or the service owning the main entity)
calls each owning service and joins the results in memory.

```ts
async function orderDetails(id: string, deadline: AbortSignal) {
  const order = await orders.get(id, { signal: deadline });
  const [customer, shipment, paid] = await Promise.allSettled([
    customers.get(order.customerId, { signal: deadline }),
    shipping.forOrder(id, { signal: deadline }),
    payments.forOrder(id, { signal: deadline }),
  ]);
  return {
    ...order,
    customer: ok(customer) ?? { id: order.customerId, unavailable: true },
    shipment: ok(shipment) ?? null,
    payments: ok(paid) ?? null,
    partial: [customer, shipment, paid].some(r => r.status === "rejected"),
  };
}
```

(The destructured result must not reuse the service's name: `const [..., payments] = await Promise.allSettled([payments.forOrder(...)])` fails `tsc --strict` with TS2448 and would throw a TDZ ReferenceError. The version above type-checks.)

## Rules
- Fan out **in parallel** where calls are independent; sequential only for true dependencies.
- Shared deadline with per-call timeouts; one slow service shouldn't hold the response.
- Decide per field whether failure is fatal or degrades (return partial with a flag).
- Batch lookups for lists (`customers.getMany(ids)`), never N+1 calls per row.
- Cache stable reference data near the composer.
- Authorization: each downstream call carries the caller's identity; don't let the composer use a
  super-user token and filter afterwards.

## Limits (when to use CQRS instead)
- Filtering/sorting/paging across services ("orders over 100 GBP for customers in Leeds, sorted by
  ship date") requires pulling large data sets into memory. Build a denormalised read model fed by
  events instead.
- High fan-out per request multiplies availability risk (5 services at 99.9% = 0.999^5 = ~99.5%, computed).
- Hot queries at high volume: a precomputed view is cheaper than repeated composition.
