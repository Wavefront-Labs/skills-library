---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.failure-domain-and-multi-region-design
name: failure-domain-and-multi-region-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, nalsd, failure-domain-design, multi-region, blast-radius]
level: advanced
status: docs-checked
description: "Design around failure domains: identify them, size replica counts and place quorum across them, and contain blast radius with sharding and shuffle sharding."
sources: ["https://sre.google/sre-book/managing-critical-state/", "https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/", "https://aws.amazon.com/builders-library/static-stability-using-availability-zones/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failure domain and multi-region design

**Goal:** any single failure takes out a bounded, known fraction of the service.

## Identify failure domains (SRE Book, Managing Critical State)
A failure domain is the set of components that can become unavailable as a result of a single failure. The book's
examples: a physical machine; a rack served by a single power supply; several racks served by one piece of
networking equipment; a datacenter that a fiber cut could take down; a set of datacenters in one geographic area
that a single natural disaster could affect. Two domains you can never escape: the software itself (bugs under
unusual circumstances) and human error by administrators (misconfiguration, mistakes, sabotage). So even solid
consensus systems spread over diverse failure domains still need regular snapshots backed up elsewhere.

## Replica counts and placement
- Majority quorums: 2f + 1 replicas tolerate f failures. The minimum is three (with two, no failure is
  tolerated). Three replicas let the system run while one is down for planned maintenance; an unplanned failure
  during maintenance makes it unavailable, so five replicas are advised, tolerating two failures.
- Placement trades the failure domains you want to survive against latency: as distance between replicas grows,
  so do round-trip time and the failure size you can survive, and for most consensus systems operation latency
  rises too.
- Do not keep widening the domain without a benefit: if all clients sit in one failure domain, surviving that
  domain's outage gains nothing because the clients are down as well.
- A sixth replica can reduce availability: with five datacenters and one replica in each, losing one leaves a
  spare; putting a sixth replica in one datacenter means an outage there removes both spares (capacity down 33
  percent in the book's example). Five replicas tolerate two unavailable (40 percent); six need a quorum of four,
  tolerating only 33 percent.
- Wide-area example: two replicas centrally in the US, one on the east coast and two in Europe lets consensus
  complete in North America without waiting for Europe, with the east coast replica as the linchpin where quorums
  overlap. Losing that replica changes latency drastically (EU to central RTT is around 50 percent higher than
  EU to east coast).
- Balance leader placement across datacenters (leaders use more outgoing bandwidth), and beware algorithms that
  cluster leaders in one datacenter, which makes failover shift traffic dramatically.

## Contain blast radius (AWS Builders' Library)
- Without sharding, a poisonous request or flood can take out one worker, then cascade through the rest as they
  absorb its work: scope of impact is everything and everyone.
- Regular sharding divides the fleet (4 shards of 2 workers), cutting scope of impact to one quarter (25 percent)
  in the article's example, at the cost of more slack capacity per shard.
- Shuffle sharding assigns each customer a virtual shard made of a random combination of workers (for example 2
  of 8). A problem customer impacts its own shard but at most one worker of any other customer's shuffle shard,
  so fault-tolerant clients with retries can keep working.
- Static stability (AWS Builders' Library): be ready for impairments before they happen. Relying on scaling up
  in other Availability Zones after one is impaired is the less effective approach; a statically stable service
  overprovisions so it keeps operating correctly without launching new instances even if a zone is impaired. The
  article distinguishes the control plane (machinery for making changes, such as launching an instance) from the
  data plane (the daily business of existing resources).

## Verify
- [ ] Failure domain table for the system with impact per domain; drills demonstrate the expected blast radius.
- [ ] After any replica-count change, recompute quorum survival for the loss of each failure domain.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Managing Critical State page (replica count, location, quorum composition, failure domains), the AWS Builders' Library shuffle-sharding article (read the introduction through the shuffle-shard explanation) and the static stability article (static stability definition and control plane versus data plane). Removed: the SRE Workbook non-abstract design source (nothing relevant on the page), the AWS cell-based architecture source (docs.aws.amazon.com not readable) and all claims about cells, N+2 stateless sizing, rollout order, and the active-passive and active-active RTO/RPO table.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
