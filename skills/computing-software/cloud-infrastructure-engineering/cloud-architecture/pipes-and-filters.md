---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.pipes-and-filters
name: pipes-and-filters
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, pipes-and-filters, processing-pipeline, filter-stages, stream-processing, pipeline-pattern]
level: practitioner
status: docs-checked
description: "Build pipes and filters pipelines: independent single-task stages joined by queues, separate scaling, idempotency, duplicate messages and when it does not fit."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/pipes-and-filters", "https://www.enterpriseintegrationpatterns.com/patterns/messaging/PipesAndFilters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipes and filters

## Structure
Decompose complex processing into **filters**, each performing a single task, connected by **pipes**. Filters are
independent, self-contained and typically stateless; each receives messages from an inbound pipe and publishes to an
outbound pipe. Filters may transform a message or test it against criteria. Pipes only connect filters: no routing
or other logic. Filters know only their input and output schemas, so they can be arranged in any order as long as one
filter's output schema matches the next one's input; a standardized schema across filters helps reordering.

## Benefits
Create new pipelines from existing filters, replace logic in one filter, reorder filters, run filters on different
hardware, run filters in parallel. A request is only as fast as the slowest filter, so run parallel instances of slow
filters (the Competing Consumers pattern). Filters need not share a datacenter. If input and output are streams,
filters can work in parallel on the stream.

## Design notes
1. A chain of message queues is a natural pipe infrastructure (the Azure example uses Queue Storage with Functions
   as filters). Use a claim check when the item is large: the pipe carries a pointer, the data sits in storage.
2. Reliability: use infrastructure that does not lose data flowing between filters.
3. Idempotency: if a filter fails after receiving a message or after posting its result, another instance may repeat
   the work, so design filters to be idempotent.
4. Repeated messages: a failed filter may post a copy of a message to the next stage, so the pipeline should detect and
   remove duplicates. Queue infrastructure such as Service Bus queues may offer duplicate detection.
5. Context: each filter runs in isolation and must be given enough context to do its work; external state adds
   load/operate/persist overhead at every filter.
6. Message tolerance: filters ignore data they do not act on and pass it along unchanged.
7. Error handling: each filter decides whether a breaking error fails the pipeline or propagates the exception.
8. Combined with Compensating Transaction, filters can implement an alternative to distributed transactions.

## Gotchas and when not to use
- Usually implemented as a monolithic pipeline: test the whole chain end to end after any change, and a failed filter
  or pipe is likely to fail the whole pipeline.
- Flexibility adds complexity, especially with filters on different servers.
- Not useful for request-response work that must complete within the initial request, for steps that are not
  independent or must be one transaction, or when per-step state makes it inefficient or causes database contention.
- Filters that should scale together can be grouped in one process (Compute Resource Consolidation).

## Verify
- [ ] Stopping one stage builds backlog in its input pipe only; restart drains it without data loss.

## Checked
2026-11-08. Confirmed against the Azure Pipes and Filters pattern page and the Enterprise Integration Patterns
Pipes and Filters page (definitions, benefits, slowest-filter bottleneck, idempotency, repeated messages, context,
message tolerance, error handling, monolithic nature, when to use or avoid, claim check example). Removed as not on
those pages: named log-stream products for pipes, dead-lettering after N attempts, correlation IDs and per-stage
metrics, Step Functions and Durable Functions orchestration, and the too-many-stages and shared-database gotchas.
Method: documentation only; no commands were run.
