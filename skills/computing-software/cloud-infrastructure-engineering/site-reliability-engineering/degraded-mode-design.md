---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.degraded-mode-design
name: degraded-mode-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [degraded-mode-design, serve-degraded-results, graceful-degradation, cascading-failures, fallbacks, feature-flags]
level: advanced
status: docs-checked
description: "Design graceful degradation: which features to drop under load, cheaper result modes, how to trigger it, and how to keep the rarely-used path working."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/", "https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Degraded-mode design

SRE Book (Addressing Cascading Failures): graceful degradation takes load shedding one step further by reducing
the amount of work per request, by decreasing the quality of responses. Its example: a search application might
search only a subset of data in an in-memory cache rather than the full on-disk database, or use a less accurate
but faster ranking algorithm when overloaded.

## Decide, per endpoint
For each critical endpoint, write down what the cheaper result is (fewer results, a cached or static copy, a
simpler algorithm), and agree it with the product owner in advance; some degradations are unacceptable (wrong prices).
The book says this must be engineered into the service and works only if you know which traffic can be degraded
and can tell payloads apart.

## Triggering (the book's questions)
- Which metrics trigger it: CPU usage, latency, queue length, number of threads used?
- Does the service enter degraded mode automatically, or by manual intervention?
- What actions are taken when degraded?
- At which layer is it implemented: every layer, or a high-level choke point?
- Provide a way to turn complex degradation off or tune its parameters quickly; the book warns that excessive
  complexity can trip a server into degraded mode when unwanted, or cause feedback cycles. Config held in a
  consistent system such as Chubby speeds deployment but adds its own risk of synchronized failure.
- Monitor and alert when too many servers enter these modes.

## Keep it working (the book's warning)
Graceful degradation should not trigger often (usually a capacity planning failure or unexpected load shift), so
keep it simple and understandable. "The code path you never use is the code path that (often) doesn't work."
The book's suggestion: regularly run a small subset of servers near overload to exercise the path.

## Gotchas
- The AWS Builders' Library explains why Amazon often avoids fallback logic: fallback paths are hard to test
  (overload scenarios are hard to replicate), are encountered rarely, and often hide latent bugs that appear
  months or years later. Prefer local, precomputed fallbacks over ones that call another dependency.
- Degraded mode must reduce load meaningfully; measure resource use per request in both modes.

## Verify
- [ ] Each critical endpoint has a documented degraded behaviour approved by product.
- [ ] Degraded mode is exercised regularly and resource per request measured lower.

## Checked

2026-11-01. Confirmed against the SRE Book chapter Addressing Cascading Failures (sections Serve Degraded Results,
Load Shedding and Graceful Degradation; the search example, the trigger questions, the code-path warning, the
exercise suggestion, the complexity warning) and the AWS Builders' Library article Avoiding fallback in
distributed systems (hard to test, rarely encountered, latent bugs). Removed: the feature table with example
figures, the CPU 85% trigger, the metric name, the stale-if-error header value, the hysteresis advice and the
one-request trigger note.
Method: documentation only; no commands were run.
