---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.shuffle-sharding
name: shuffle-sharding
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, fault-isolation, shuffle-sharding, blast-radius, poison-pill-requests, tenant-isolation, combinatorial-isolation, noisy-neighbour]
level: advanced
status: docs-checked
description: "Limit the blast radius of poison requests and noisy tenants by assigning each customer a random small subset of workers: shard maths, routing, and when it's worth it."
sources: ["https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_fault_isolation_use_bulkhead.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shuffle sharding

## Idea
Take a horizontally scalable service of 8 workers (servers, queues or databases). With no sharding a failure
triggered by one kind of request, or by a flood such as a DDoS attack, takes out the first worker and then cascades as
the survivors take over: the scope of impact is everything and everyone. Ordinary sharding into 4 shards of 2 workers
cuts the impact to a quarter, at the cost of more slack capacity because each shard has only two workers.

Shuffle sharding creates virtual shards: each customer (or resource) is assigned a combination of workers, 2 of the 8
in the Builders' Library example. A problem customer hits only its own virtual shard; at most one worker of any other
customer's shard is affected, so fault-tolerant clients that retry still get service from their other worker. Eight
workers give 28 unique pairs, so with hundreds of customers spread over them the scope of impact is 1/28, which the
article calls 7 times better than regular sharding. The gain grows with more workers and customers, and with enough
workers there can be more shuffle shards than customers so each is isolated.

## Steps
1. Choose the number of workers (or cells, queues) and the shard size k per customer. The number of combinations is
   C(N,k), for example C(100,5) = 75,287,520.
2. Assign each customer a shuffle shard. Route 53's design (per the article) arranges capacity into 2048 virtual name
   servers and gives each domain a shuffle shard of 4, about 730 billion possible shards, and ensures no two domains
   share more than two virtual name servers. Virtual servers can be moved to manage capacity.
3. Route requests for a customer only to its k workers; requestors need to be fault tolerant (for example retries) so
   they work around the affected worker.
4. A targeted customer can then be identified and moved to special dedicated attack capacity (as Route 53 does).
5. Refinement named in the article: recursive shuffle sharding, sharding at multiple layers to isolate a customer's
   customer. The article points to the open source Route 53 Infima library for implementations.

## Related: cell-based design (AWS Well-Architected REL10-BP03)
Cell-based (bulkhead) architectures partition the workload by a partition key such as customer ID or resource ID that
is present in all requests; a router layer maps keys to cells (the guide suggests cryptographic hash functions with
modular arithmetic) and must stay simple and horizontally scalable. Keep the mapping persistent, give cells a tested
maximum size, do not share state between cells, and deploy to cells in a staggered way rather than all at once.

## When worth it
Multi-tenant services where one customer's traffic or inputs can crash or saturate workers. The article says shuffle
sharding usually comes at no additional cost since it rearranges existing resources.

## Gotchas
- Routing must be possible by customer key.
- Smaller shards mean less slack: size the shard for the customer's needs.

## Verify
- [ ] Simulated poison customer affects only customers sharing their full shard.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Amazon Builders' Library article (8 workers, 28 combinations, 1/28 and 7x, Route 53 2048 virtual
name servers, shard of 4, 730 billion, max two shared, Infima, recursive sharding) and REL10-BP03 (partition key,
router, cell size, staggered deployment). Removed: hash(customer_id) seeding and consistent-hash claims, per-customer
throttling advice and "capacity per customer is k workers" (not in the pages). C(100,5) is arithmetic.
