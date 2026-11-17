---
id: computing-software.cloud-infrastructure-engineering.observability.controlling-trace-volume-and-sampling-cost
name: controlling-trace-volume-and-sampling-cost
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [trace-volume, sampling-ratio-cost, observability-cost, sampling, tail-sampling]
level: advanced
status: docs-checked
description: "Decide whether and how to sample traces to control cost: head vs tail sampling trade-offs, tail sampling policies, and the costs sampling itself adds."
sources: ["https://opentelemetry.io/docs/concepts/sampling/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlling trace volume by sampling

## Should you sample? (OpenTelemetry sampling concepts)
Sampling is described as one of the most effective ways to reduce observability cost without losing visibility,
because it preserves representativeness; high-volume systems often represent the rest accurately at 1% or lower.
Consider it if you:
- generate 1000 or more traces per second, mostly healthy and low-variation;
- have criteria (errors, high latency, domain rules) that mark interesting traces;
- can tell services apart so high- and low-volume ones sample differently;
- can route unsampled data to low-cost storage for "just in case".
Avoid it if you generate tens of small traces per second or fewer, only use aggregated data, or regulation
prohibits dropping data. Sampling has its own costs: compute for a tail sampler, engineering upkeep, and the
opportunity cost of missing critical data. It can be cheaper to allocate more resources instead.

## Head sampling
Decision made as early as possible without inspecting the whole trace. The common form is consistent probability
sampling (deterministic, from trace ID and a percentage), which keeps whole traces. Upsides: easy to understand and
configure, efficient, can be done anywhere in the pipeline. Downside: you cannot guarantee that traces containing
errors are sampled.

## Tail sampling
Decision made considering all or most spans of a trace: always keep error traces, sample by overall latency, by
attribute presence or value, or apply different rates by criteria. Downsides: hard to implement, hard to operate
(stateful, stores a lot of data, may need dozens or hundreds of nodes and fall-back strategies, must be monitored),
and often vendor-specific. Systems with extreme volume may head sample first, then tail sample later in the
pipeline, often to protect the telemetry pipeline from overload.

## Collector tail sampling processor
All spans of a trace must reach the same collector instance for effective decisions. Settings: `decision_wait`
(default 30s), `num_traces` (default 50000, traces kept in memory), `expected_new_traces_per_sec`, `policies`.
Policy types include `latency` (`threshold_ms`, optional `upper_threshold_ms`), `status_code`, `string_attribute`,
`probabilistic` (`sampling_percentage`), `rate_limiting`, `bytes_limiting`, `span_count`, `ottl_condition`, `and`,
`not`, `drop` and `composite` (rate allocation per policy).
```yaml
processors:
  tail_sampling:
    decision_wait: 10s
    num_traces: 100000
    policies:
      - name: errors
        type: status_code
        status_code: {status_codes: [ERROR]}
      - name: slow
        type: latency
        latency: {threshold_ms: 1000}
      - name: baseline
        type: probabilistic
        probabilistic: {sampling_percentage: 5}
```
When a trace is sampled, the processor rewrites each span's `th` threshold to the smallest effective threshold among
the policies that voted to sample.

## Verify
- [ ] Rules for errors and latency keep the traces on-call needs, tested against known incidents.
- [ ] The tail sampler's memory and decision behaviour are monitored.

## Checked
2026-11-09. Confirmed against the opentelemetry.io sampling concepts page (why, when, head and tail sections read
from markdown source) and the tail sampling processor README (config options, policy types, tracestate behaviour).
Removed unconfirmed claims and the Grafana source (not read): span-size and bytes-per-day estimates, Tempo and
collector metric names, RED metric ordering advice, SDK sampler environment variable recipe, ratio-choosing
heuristics, tail sampler memory formula and the loadbalancing exporter hint.
Method: docs-checked 2026-11-09 against the opentelemetry.io sampling concepts markdown and the tailsamplingprocessor README; documentation only, no commands run.
