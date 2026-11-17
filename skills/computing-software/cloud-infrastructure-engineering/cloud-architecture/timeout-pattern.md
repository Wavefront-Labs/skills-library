---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.timeout-pattern
name: timeout-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resiliency-patterns, timeout-pattern, timeouts, deadline-propagation, connect-timeout, request-timeout, timeout-budget]
level: practitioner
status: docs-checked
description: "Set timeouts on every remote call: connect vs request timeouts, sizing from the downstream's latency percentile, gRPC deadline propagation and not stacking retries on timeouts."
sources: ["https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/", "https://grpc.io/docs/guides/deadlines/", "https://learn.microsoft.com/azure/architecture/patterns/retry"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeout pattern

## Rules
1. **Every** remote call, and generally any call across processes even on one box, gets a timeout: both a
   connection timeout and a request timeout. Clients without one can hold threads, connections and memory
   while a struggling dependency stalls. gRPC sets no deadline by default, so a client can wait effectively
   forever; always set a realistic one.
2. **Sizing within a region**: choose an acceptable false-timeout rate (the AWS example is 0.1%) and take the
   matching latency percentile of the downstream service (p99.9 in that example).
   - Over the internet, add reasonable worst-case network latency.
   - Where p99.9 is close to p50, add padding so small latency rises do not cause mass timeouts.
   - Too high wastes resources while waiting; too low drives extra retries and can turn a small latency
     increase into an outage.
   - For gRPC start from an educated guess about network latency and server time, validated by load testing.
3. **Deadline propagation**: a server that calls another server should honour the original client's deadline.
   gRPC converts the deadline into a remaining timeout on each hop, avoiding clock skew. Java and Go enable
   propagation by default; C++ needs it enabled explicitly. Servers must stop work they spawned once the
   call is cancelled.
4. **Check what the timeout covers.** Some implementations do not cover DNS or TLS handshakes; prefer
   well-tested client timeouts. AWS describes a low timeout that included new secure connection setup and
   caused timeouts after deployments; they opened connections at process start, before traffic.
5. **Retries**: retry at a single layer (see retry-pattern); a timeout does not mean a side effect did not
   happen, so retry only idempotent calls.

## Gotchas
- Retrying after a timeout on a non-idempotent call.
- Timeouts so tight they fail during cold starts or connection setup.

## Verify
- [ ] Injected dependency latency triggers timeouts and fallbacks; threads do not pile up.
- [ ] Every client has an explicit connect and request timeout or deadline.

## Checked
2026-11-01. Confirmed against the AWS Builders' Library article (timeout sizing, pitfalls, connection-setup
example), the gRPC Deadlines guide (no default deadline, propagation, languages) and the Azure Retry page.
Removed: the 1-2 s connect-timeout figure, Java/PostgreSQL/gRPC code examples, the "inner shorter than
outer" ordering, the load balancer idle-timeout rule and the "timeout x attempts" formula, none of which
those pages state.
Method: documentation only; no commands were run.
