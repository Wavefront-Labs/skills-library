---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.stateless-design
name: stateless-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, scalability, stateless-design, session-externalisation, distributed-session-store, jwt-sessions, sticky-sessions, horizontal-scaling, websocket-scaling]
level: practitioner
status: docs-checked
description: "Make an app tier stateless to scale out: avoid instance stickiness, keep session and persistent data in backing services, and design for instances being added and removed."
sources: ["https://learn.microsoft.com/azure/architecture/guide/design-principles/scale-out", "https://12factor.net/processes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stateless tier design

## Principles
- **Avoid instance stickiness** (session affinity). It limits scale-out because a high-volume user's traffic
  is not spread across instances. Causes include in-memory session state and machine-specific encryption
  keys. Any instance must be able to handle any request.
- **Twelve-factor processes are stateless and share-nothing.** Data that must persist goes in a stateful
  backing service, typically a database. Memory and local disk are only a brief single-transaction cache;
  never assume a later request or job sees what was cached, because a different process may serve it and a
  restart wipes local state.
- **Sticky sessions violate twelve-factor** and should not be relied upon. Session state suits a datastore
  with time-expiration such as Memcached or Redis (the 12factor page's examples).
- **Do asset compilation at build time**, not into a runtime filesystem cache.

## Migration steps
1. Inventory per-instance state: sessions, generated or uploaded files, in-memory caches treated as truth,
   local locks and connection maps.
2. Move sessions and other persistent state to a backing service with expiry where appropriate.
3. Keep local caches as an optimisation only.
4. Identify bottlenecks first; stateful parts are the most likely cause, and adding web servers does not
   help if the database is the bottleneck.
5. Design for scale in: handle shutdown events cleanly, have clients retry transient faults, break long tasks
   into checkpointed pieces, and put work items on a queue so another instance can resume them.
6. Offload asynchronous and resource-heavy work to message-driven background jobs.

## Gotchas
- A session store outage affects every user; plan for its availability.
- Sticky sessions can look free but block scale-in and spread load unevenly (stickiness limits scale-out per
  the Azure guidance).

## Verify
- [ ] Stickiness is disabled and any instance can serve any request.
- [ ] Removing an instance during load causes no lost work or user-visible errors.

## Checked
2026-11-01. Confirmed against the Azure "Design to scale out" principles page and the 12factor.net
Processes page. Removed: the cookie size figure, JWT versus session-store comparison, specific product names
other than the page's Memcached and Redis, the WebSocket backplane options and the "3 instances" test rule,
none of which those pages state. Dropped the AWS web-hosting whitepaper source, which returned no relevant
text.
Method: documentation only; no commands were run.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.twelve-factor-processes
