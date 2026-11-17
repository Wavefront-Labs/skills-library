---
id: computing-software.software-engineering.software-architecture.pipes-and-filters-architecture
name: pipes-and-filters-architecture
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-styles, pipes-and-filters, pipeline-architecture, data-pipelines, stream-processing]
level: practitioner
status: verified
description: "Structure processing as pipes and filters: single-purpose filters, typed pipes, backpressure, error channels and when a pipeline beats a layered design."
sources: ["https://www.enterpriseintegrationpatterns.com/patterns/messaging/PipesAndFilters.html", "https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters", "https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipes and filters architecture

**Shape:** data flows through a chain of independent **filters** (each does one transformation) linked
by **pipes** (in-process streams, queues, topics). Unix shells, compilers, ETL, media transcoding,
log processing (Logstash/Vector), Kafka Streams topologies.

## Common filter roles
Producer (source) -> Transformer (map) -> Tester (filter/route) -> Consumer (sink).

## Design rules
- Each filter is stateless where possible, with one input and one output contract (schema per pipe).
  Stateful steps (dedupe, windowed aggregation) are explicit and own their state store.
- Pipes are one-way. Branching = a router filter; joining = an explicit merge filter.
- Make filters independently deployable and scalable when pipes are queues: scale the slow stage
  only (Azure pattern).
- **Backpressure**: bounded buffers between stages; when a sink is slow, upstream blocks or sheds
  (Reactive Streams, Go channels with capacity, Kafka consumer lag as the buffer).
- **Errors**: route bad records to a dead-letter pipe with the error and original payload; don't
  stop the pipeline for one record. Make filters idempotent so replays are safe.
- **Ordering**: only guaranteed within a partition/key; parallel filters reorder.
- Observability per stage: throughput, latency, error rate, queue depth.

## When to choose
Good: sequential transformations, reusable steps, batch or streaming data. Poor: interactive
request/response with many cross-cutting interactions, or when stages need shared mutable state
(then it's really a layered or event-driven system).

## Sketch (Python generators, in-process)
```python
def read(path):   yield from open(path)
def parse(lines): return (json.loads(l) for l in lines if l.strip())
def valid(recs):  return (r for r in recs if r.get("user_id"))
def write(recs, out): [out.write(json.dumps(r) + "\n") for r in recs]
write(valid(parse(read("in.ndjson"))), sys.stdout)
```
Lazily evaluated, constant memory (run: the record without `user_id` and the blank line were dropped); same shape scales out with queues between stages. The Azure Pipes and Filters page says filters can be deployed and scaled independently, and that filters should be idempotent because a failed filter can cause the next stage to see data twice.
