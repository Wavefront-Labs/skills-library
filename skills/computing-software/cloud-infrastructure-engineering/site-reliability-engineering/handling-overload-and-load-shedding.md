---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.handling-overload-and-load-shedding
name: handling-overload-and-load-shedding
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, overload, handling-overload, load-shedding, adaptive-throttling, client-side-throttling, criticality, request-criticality, per-customer-quotas, utilization-signals, graceful-degradation, degraded-mode, retry-budget, load-management]
level: advanced
status: docs-checked
description: "Keep a service useful under excess load per the SRE Book: CPU-based capacity, per-customer quotas, adaptive client throttling, criticality tiers, retry rules."
sources: ["https://sre.google/sre-book/handling-overload/", "https://sre.google/sre-book/addressing-cascading-failures/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling overload and load shedding

**Goal:** when demand exceeds capacity, serve what the system can, reject the rest cheaply, and do not let
overload make things worse. Everything below is from the SRE Book chapter Handling Overload unless noted.

## 1. Model capacity in resources, not QPS
Queries differ widely in cost, and ratios drift over time, so queries per second (or static proxies such as
keys read) make a poor capacity metric. Measure directly in resources; speak of a request's "cost" as normalised
CPU time. CPU consumption works as the provisioning signal in most cases (GC memory pressure shows up as CPU;
other resources can be provisioned to outlast CPU); where that is too costly, account for each resource
separately.

## 2. Per-customer limits
Under global overload, only misbehaving customers should get errors. Define per-customer quotas from negotiated
usage (in CPU seconds per second); they may sum to more than capacity because customers rarely all peak
together. Aggregate usage in real time and push effective limits to backend tasks. Limits can be set per
criticality.

## 3. Client-side adaptive throttling
Rejecting costs resources too, so a backend can end up spending most of its CPU rejecting. When a client sees
many recent "out of quota" rejections it caps its own outgoing traffic; excess requests fail locally. Each
client task keeps, for the last two minutes, `requests` (attempted by the application layer) and `accepts`
(accepted by the backend). Normally equal; once requests exceed K times accepts, new requests are rejected
locally with a probability that rises as requests outgrow accepts. K is tunable: lower K is more aggressive.
The book prefers 2x because it propagates "backend recovered" faster at the cost of some wasted backend work,
and reports backends rejecting about one request per request processed in large overloads. It may work poorly
for clients that send only sporadically. The decision uses only local information.

## 4. Criticality
Every request carries one of four values:
- `CRITICAL_PLUS`: serious user-visible impact if it fails.
- `CRITICAL`: default for production requests; services provision for all expected CRITICAL and CRITICAL_PLUS.
- `SHEDDABLE_PLUS`: partial unavailability expected; default for batch jobs that can retry later.
- `SHEDDABLE`: frequent partial and occasional full unavailability expected.
Overloaded tasks reject lower criticalities sooner; quota enforcement rejects a criticality only if already
rejecting all lower ones; adaptive throttling keeps stats per criticality. Criticality is separate from
latency need, and is propagated to downstream calls by default. Set it as close to the user as possible (HTTP
frontends) and override only where it makes sense.

## 5. Task-level utilization signals
Reject based on local utilization, with higher thresholds for higher criticality. Utilization is often CPU
rate over reserved CPUs, sometimes plus memory. The most generally useful signal is "executor load average":
count active threads (running or ready and waiting for a processor), smooth with exponential decay, and start
rejecting when active threads exceed available processors; smoothing absorbs short fan-out spikes. Signals can
be combined. Each task must be protected: a task provisioned for a rate should keep serving that rate
regardless of excess traffic (the book says somewhere above 2x or even 10x), and an overloaded backend should
keep accepting what it can, not turn everything down.

## 6. Degrade and retry sensibly
- Serve degraded responses (search a subset, use a possibly stale local copy) before serving errors.
- If a large subset of tasks is overloaded, do not retry; bubble the error up. If a small subset is, retry
  immediately: retries are indistinguishable from new requests to the balancer and act as organic balancing.
- Per-request retry budget of up to three attempts; per-client budget: retry only while the retry ratio is
  below 10 percent, which in the book's worst case cuts growth from almost 3x to about 1.1x.
- A retry counter in request metadata lets backends return "overloaded; don't retry" when histograms show
  other tasks overloaded too.
- Retry only at the layer directly above the rejecting one, to avoid a combinatorial retry explosion.

## 7. Connections
Connection pools and connection churn cost CPU and memory; idle health checking from many low-rate clients can
cost more than the requests. Tune health checks or create connections dynamically. For bursts from huge batch
jobs, expose load to cross-datacenter balancing, or force batch clients through a batch proxy that acts as a
fuse.

## Checked
2026-11-01. Confirmed against the SRE Book chapters Handling Overload (read in full) and Addressing Cascading
Failures. Removed: the explicit rejection-probability formula (not in the page text), Envoy, Netflix and
Kubernetes recipes, the whole autoscaling section, metric names, header names and verify targets, none stated
by those chapters.
Method: documentation only; no commands were run.
