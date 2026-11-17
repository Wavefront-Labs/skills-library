---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.server-queue-management-codel-and-adaptive-lifo
name: server-queue-management-codel-and-adaptive-lifo
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, handling-overload, codel-queue, adaptive-lifo, queue-management, load-shedding]
level: advanced
status: docs-checked
description: "Manage server request queues under overload with bounded queues, CoDel or LIFO queueing, load shedding and deadline checks so latency stays bounded."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/", "https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server queue management: CoDel and LIFO

**Goal:** when demand exceeds capacity, serve some requests fast instead of all requests too late.

## Why queues hurt
Queued requests consume memory and increase latency. If the queue is 10x the number of threads and a request
takes 100 ms on a thread, a request arriving at a full queue takes 1.1 seconds, mostly spent waiting. If request
rate and latency were constant there would be no reason to queue at all.

## Techniques (SRE Book, Addressing Cascading Failures)
1. **Bounded queue, small for steady traffic**: for a service with fairly steady traffic, keep queue length small
   relative to the thread pool (the book suggests 50 percent or less) so the server rejects early when it cannot
   sustain the incoming rate. Gmail often uses queueless servers and relies on failover to other tasks when
   threads are full. Systems with bursty load may need a queue sized from threads in use, processing time and
   the size and frequency of bursts.
2. **Per-task throttling**: shed load based on CPU, memory or queue length; for example return HTTP 503 to any
   request when more than a given number of client requests are in flight.
3. **LIFO or CoDel instead of plain FIFO**: switching the queue from FIFO to last-in-first-out, or using the
   controlled delay (CoDel) algorithm or similar, removes requests unlikely to be worth processing. If an RPC
   has been queued for 10 seconds the user has probably given up and refreshed, so answering the first request
   is wasted work. This works best combined with propagating RPC deadlines through the stack.
4. **Deadline checks**: do not do work for a request whose deadline has passed; check the remaining deadline
   before each stage of multi-stage handling (the book's example: parsing, backend request, processing).
5. **Fail fast**: if a backend is unavailable, return an error immediately rather than holding resources until
   the deadline.

Backlog behaviour from the AWS Builders' Library: real-time systems are often built with FIFO-ish queues but
users prefer LIFO-ish behaviour; when faced with a backlog they want fresh data processed immediately, and data
accumulated during an outage or surge can be processed as capacity allows.

## Tuning
The CoDel interval, target queueing delay and shorter timeout while overloaded are parameters you set and
measure for your service; this skill does not give numeric defaults. Read the original CoDel paper for the
algorithm, and test with a load test beyond capacity.

## Verify
- [ ] Load test beyond capacity: goodput stays near capacity, latency of served requests stays bounded, rejected requests fail fast; queue length metric stays bounded.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Addressing Cascading Failures page (queue management, load shedding, LIFO/CoDel, deadline and fail-fast sections) and the AWS Builders' Library page on insurmountable queue backlogs (LIFO-ish preference). Removed: the 100 ms interval and 5 ms target numbers, the pseudocode, the Facebook attribution, and the Netflix and Envoy adaptive concurrency limiter claims, because the Facebook and ACM Queue pages could not be read (404 and 403) and the limiter docs were not read.

Method: docs-checked 2026-11-09 against the pages above, read in full from downloaded copies; no commands were run.
