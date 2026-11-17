---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.non-abstract-large-system-design
name: non-abstract-large-system-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, nalsd, non-abstract-large-system-design, system-design, system-design-estimation, back-of-the-envelope, capacity-estimation, napkin-math, latency-numbers, qps-estimation, storage-estimation, bottleneck-analysis, sharding, replication, design-review, scalability, fault-tolerance, cost-estimation, iterative-design, design-interview, resource-model, headroom]
level: advanced
status: docs-checked
description: "Design large systems with numbers attached (SRE Workbook NALSD): the iterative method from basic design to scale and resilience, turning a whiteboard into resource estimates."
sources: ["https://sre.google/workbook/non-abstract-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-abstract large system design (NALSD)

**Goal:** a design that states how many machines, how much storage and bandwidth, and where it breaks, so reviewers
can check the arithmetic instead of nodding at boxes and arrows. The Workbook defines NALSD as an iterative style
of design that combines elements of capacity planning, component isolation and graceful degradation, and expects
SREs to start resource planning from a basic whiteboard diagram and think through scaling and failure domains.

## 1. The method (SRE Workbook)
Two phases, each with two to three questions:
1. **Basic design**: *Is it possible?* (ignoring RAM, CPU and network limits, what would satisfy the requirements?)
   and *Can we do better?* (faster, smaller, more efficient; e.g. a better algorithm complexity).
2. **Scale up**: *Is it feasible?* (given money and hardware, what distributed design satisfies the requirements?),
   *Is it resilient?* (what happens when a component fails, or a whole datacenter?) and *Can we do better?*
Practice bounces between the questions; when a design flounders you modify or replace components. Each iteration is
written down with its assumptions and checked against the requirements, expressed as SLOs.

## 2. The worked example (AdWords click-through rate)
Requirements: 500,000 search queries/s, 10,000 clicks/s; 99.9% of dashboard queries under 1 second; data less than
5 minutes old 99.9% of the time. Iterations: one machine (rejected: 86.4 TB/day of logs, 200 IOPS per HDD, single
points of failure); MapReduce (scales, misses freshness SLO); LogJoiner with QueryStore, ClickMap, QueryMap;
sharded and duplicated LogJoiner; multi-datacenter with Paxos-replicated ClickMap. See the `nalsd-*` skills for
each step.

## 3. Estimation habits (from the chapter)
- Use scientific notation to limit unit errors; round up aggressively and state each assumption.
- Reasoning and sound assumptions matter more than a perfect final value; early assumptions heavily influence
  results.
- Check the final design against every requirement, and ask what happens when each component fails.

## 4. Scaling moves seen in the chapter
- **Sharding**: hash a key (modulo the shard count) so each instance sees a consistent subset; shard by the key known
  before reads and writes.
- **Replication**: send records to two shards, on different machines, so a failure does not stall results.
- **Consensus**: a replicated store across datacenters using Paxos costs at least one round trip per write, which
  limits sequential throughput.

## 5. Reviewing a design
Where is the number for each requirement? What breaks first? What is the blast radius of losing a shard or
datacenter? Which assumption, if wrong, breaks the design? (Review questions are advice; the chapter's own
questions are in section 1.)

## Gotchas
- Skipping the one-machine step hides which resource really binds.
- Replicating work changes downstream rates; recompute after every iteration.
- Designing the hot path through a single point of failure.

## Verify
- [ ] The design doc has a numbers section: load, per-machine capacity with its source, machine counts, storage and
  bandwidth, and the named bottleneck.
- [ ] Failure scenarios (shard loss, datacenter loss) have numbers, not adjectives.

## Checked
2026-11-01. Confirmed against the SRE Workbook chapter "Introducing Non-Abstract Large System Design": definition, the two phases and four-five questions, AdWords requirements and SLOs, iterations, hash-modulo sharding, duplicate shards, Paxos round trip limit, scientific notation and rounding advice.
Removed: the latency constants table, per-core and peak-factor rules of thumb, the thumbnail-service skeleton, headroom and N+2 rules, and three sources that did not state the removed figures.
Method: documentation only; no commands were run.
