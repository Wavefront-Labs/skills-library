---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.geode-pattern
name: geode-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resiliency-patterns, geode-pattern, geodes, multi-region-active-active, global-load-balancing, geo-distributed-backend]
level: advanced
status: docs-checked
description: "Deploy geodes: identical backend deployments in many regions behind global routing, any geode serves any request, with a geo-replicated data store and a conflict policy."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/geodes", "https://learn.microsoft.com/azure/cosmos-db/distribute-data-globally"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geode

## Idea
Deploy a backend service into several geographic nodes (geodes); each can serve any request from any client in any region. This active-active approach brings compute to the data to cut latency and raise availability. A global routing service distributes requests by routing policy and health checks, and every geode accesses a geo-replicated data store.

Characteristics (Azure Architecture Center): each geode is a set of resources often defined in a deployment template; it holds the regional resources needed to serve requests without depending on another geode's application tier (shared routing and data services can still exist); geodes are loosely coupled through global routing and a replication backplane.

## Design steps
1. Create identical geodes with DevOps tooling and the same pipeline.
2. Pick a geo-replicated data store and consistency level. Geodes can see different versions of an item during replication, so the application must handle replication lag and concurrent writes, especially when a client moves between geodes. Select a conflict resolution policy for concurrent writes.
3. Global routing with health checks. For Azure Front Door, give concurrently active geodes the same priority, then set latency sensitivity and weights.
4. Define the failure modes to tolerate (regional outages, shared dependency failures). Availability depends on healthy shared dependencies and enough compute and database capacity in surviving geodes for redirected traffic, so size for the redirected peak.
5. Test regional failover, recovery and failback under representative load in a controlled environment.
6. Use autoscaling within each geode and zone-redundant resources where supported. Choose regions for latency, data residency, service availability and recovery needs.

## Cosmos DB example
With multi-region writes, each region serves reads and writes; replication is asynchronous. Configure the SDK so each geode reads and writes to its local region with fallback regions. With session consistency, return the session token to the client and have it send the token on later reads so read-your-writes survives a move to another geode; in multi-region-write accounts use the shared tokens only for reads. The Cosmos DB docs also state serverless accounts run in a single region only, and that regions can be added or removed without pausing or redeploying the application.

## Secure and observe
- Restrict database access to the compute tier; in the Azure example, public function app origins behind Front Door combine the `AzureFrontDoor.Backend` service tag with an `X-Azure-FDID` header filter in one allow rule. Keep caller authentication separate.
- Give each geode access to the secrets it needs and coordinate rotation of shared secrets.
- Track one request across geodes and monitor shared dependencies to spot correlated failures.

## Geodes versus deployment stamps
Stamps serve an assigned subset of users or tenants; a geode serves the same operations for any user and can reach the data needed. Choose by request eligibility and data placement.

## When not to use
- Regional data-residency or other restrictions tie users or data to particular deployments (consider stamps with data-aware routing).
- A single region meets requirements (consider zone redundancy and separate regional DR).
- Session state or data dependencies bind requests to one region; existing apps may need state, replication and automation changes first.
- Latency and availability needs do not justify geo-distribution.

## Verify
- [ ] Taking one geode out of routing shifts traffic with errors inside tolerance and survivors handle the load.
- [ ] A client moved between geodes still sees its own writes where required.
- [ ] Concurrent cross-region writes resolve by the chosen policy.

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Geode pattern (last updated 2026-11-07); Azure Cosmos DB, Distribute your data globally (updated 2026-04-27).
Removed as unconfirmed: named non-Azure equivalents (CloudFront, Global Accelerator, global ALB, DynamoDB global tables, Spanner), "last writer wins" as the stated policy, and the "size each geode to absorb one failed neighbour" rule (replaced by the page's sizing wording).
Method: documentation only; no commands were run.
