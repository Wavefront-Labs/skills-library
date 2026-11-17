---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.launch-dependency-review
name: launch-dependency-review
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [launch, dependencies, launch-checklist, capacity, failure-modes]
level: practitioner
status: docs-checked
description: "Review a launch's internal and external dependencies using Google SRE Book launch checklist themes: architecture, capacity, failure modes, clients, external dependencies."
sources: ["https://sre.google/sre-book/launch-checklist/", "https://sre.google/sre-book/reliable-product-launches/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Launch dependency review

**Goal:** no launch fails because a dependency was not ready for the new load or behaviour.

## Where the sources put dependencies
The SRE Book's launch checklist chapter says an architecture review identifies the owners of shared infrastructure as additional stakeholders in the launch, and that the dependency list from this section can be used in later capacity planning to make sure every dependency is correctly provisioned. The original 2005 checklist (appendix) has "Architecture", "System reliability and failover" and "External dependencies" sections.

## Inventory table (your own format)
For each dependency, note whether it is hard or soft, expected new load, quota or limit, owner contacted, failure behaviour and fallback. The sources give the questions below, not a table.

## Questions from the SRE Book
Architecture:
- What is your request flow from user to frontend to backend? Are there request types with different latency requirements?
- Actions: isolate user-facing from non-user-facing requests; validate request volume assumptions, since one page view can become many requests.

Capacity:
- Is the launch tied to a press release, advertisement or blog post? How much traffic and growth do you expect during and after launch? Have you obtained all compute resources?
- Launch spikes can differ in traffic mix from steady state; the book says some products had to handle spikes up to 15 times the initial estimate, and launching region by region builds confidence.
- Redundancy: if three replicated deployments serve peak traffic, keep four or five.

Failure modes:
- Any single points of failure? How do you mitigate unavailability of dependencies, at startup and at runtime? Can the service serve in degraded mode if a dependency fails?
- Actions: implement request deadlines; implement load shedding.

Client behaviour:
- Do clients back off exponentially on failure and jitter automatic requests? A client syncing every 60 seconds instead of 600 causes ten times the load.

External dependencies:
- What third-party code, data, services or events does the launch depend on? Do partners depend on you and need notification? What if you or the vendor cannot meet a hard deadline?
- The book says filtering or rewriting proxies, data transcoding pipelines and caches have been used to mitigate vendor risks.

The 2005 checklist also asks: how to detect when backends die and what to do; graceful degradation; how to avoid accidentally overrunning third-party services; load balancing, rate-limiting, timeout, retry and error handling; and impact on the other services you care most about.

## Verify
- [ ] Each hard dependency has a named owner who has confirmed capacity for the new load.
- [ ] Failure behaviour of each dependency is known, ideally exercised in a test (the book says load testing is required for most launches).

## Checked
Confirmed against the SRE Book "Reliable Product Launches at Scale" (Architecture and Dependencies, Capacity Planning, Failure Modes, Client Behavior, External Dependencies, Dealing with Abusive Client Behavior, Overload Behavior) and the "Launch Coordination Checklist" appendix. Removed: the sample dependency table values, the 15-minute cached-session fallback, SLO-versus-dependency rule and quota/maintenance-window questions, which the sources do not state.
Method: docs-only read of cited pages, 2026-11-08
