---
id: computing-software.cloud-infrastructure-engineering.observability.otel-head-and-tail-sampling-configuration
name: otel-head-and-tail-sampling-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [head-sampling, tail-sampling, trace-id-ratio-sampler, parent-based-sampler, otel-traces-sampler-env, tail-sampling-policies, tail-sampling-processor, probabilistic-sampler-processor, hash-seed-sampling, composite-sampling-policy, and-policy, sampling-adjusted-counts, sampling-and-span-metrics]
level: advanced
status: docs-checked
description: "Configure trace sampling end to end: SDK ParentBased/TraceIdRatio samplers, collector probabilistic and tail sampling policies (and, composite), and keeping span metrics correct."
sources: ["https://opentelemetry.io/docs/concepts/sampling/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/probabilisticsamplerprocessor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Head and tail sampling configuration

## Head sampling (SDK)
```bash
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1          # 10% of new traces; children follow the parent's decision
```
`parentbased_traceidratio` is `ParentBased(root=TraceIdRatioBased)`; `OTEL_TRACES_SAMPLER_ARG` is a probability in [0..1] (default
1.0), and the spec default sampler is `parentbased_always_on`. When the collector does tail sampling, the SDK must send the
spans it should decide on, so do not drop them at the SDK.

## Probabilistic sampler (collector)
```yaml
processors:
  probabilistic_sampler:
    sampling_percentage: 15
    hash_seed: 22            # same seed on every collector -> consistent per trace ID across instances
    mode: proportional       # hash_seed (default) | proportional | equalizing; the latter two use the OTel threshold/randomness
```
Stateless: it decides per item, not per whole trace (the README points to the tail sampling processor for whole-trace sampling).
Stability: beta for traces, alpha for logs. In `hash_seed` mode (the default; seed 0 if unset) all collectors of a tier must share
the same `hash_seed`. `proportional` outputs about `sampling_percentage` of the input regardless of earlier sampling;
`equalizing` accounts for how much an item was already sampled. In every mode the effective probability is written into the
tracestate (`ot=th:...`, optional `rv`). A `sampling.priority` attribute overrides the decision: 0 means drop, non-zero means keep
for traces. For logs, `attribute_source` and `from_attribute` choose the randomness source (trace ID or a record attribute).

## Tail sampling (collector)
```yaml
processors:
  tail_sampling:
    decision_wait: 10s                 # default 30s; time before the decision timer fires for a trace
    num_traces: 100000                 # default 50000; traces held in memory
    expected_new_traces_per_sec: 2000  # default 0; sizes data structures
    policies:
      - {name: errors, type: status_code, status_code: {status_codes: [ERROR]}}
      - {name: slow, type: latency, latency: {threshold_ms: 1000}}
      - name: checkout-sampled
        type: and
        and:
          and_sub_policy:
            - {name: svc, type: string_attribute, string_attribute: {key: service.name, values: [checkout]}}
            - {name: pct, type: probabilistic, probabilistic: {sampling_percentage: 20}}
      - {name: baseline, type: probabilistic, probabilistic: {sampling_percentage: 2}}
```
A trace is sampled if a policy returns "sample", and not sampled when a `drop` policy decides so or when no policy samples it.
The `not` and `drop` policies replace the deprecated `invert_match` behaviour. The `composite` policy splits
`max_total_spans_per_second` across sub-policies by `rate_allocation` percentages. Other policy types include `always_sample`,
`numeric_attribute`, `trace_state`, `trace_flags`, `rate_limiting`, `bytes_limiting`, `span_count`, `boolean_attribute` and
`ottl_condition`. Place the processor after processors that need span context (for example `k8sattributes`), because it reassembles
spans into new batches. **All spans of a trace must reach the same collector instance** (README warning): front tail-samplers with
the `load_balancing` exporter (routing key `traceID`). `decision_cache` (`sampled_cache_size`, `non_sampled_cache_size`, default 0)
keeps decisions for late spans.

## Keeping metrics correct
- Generate span metrics and service graphs from unsampled spans, before the sampling step, or request counts undercount.
- If you must compute from sampled data, use adjusted counts (1 / sampling probability); the samplers record the threshold in
  the tracestate `ot=th:` field for that purpose (the example in the README: 25% sampling is `ot=th:c`).

## Verify
- [ ] `otelcol_processor_tail_sampling_sampling_decision_timer_latency` and `..._count_traces_sampled` look sane;
  `otelcol_processor_tail_sampling_sampling_trace_dropped_too_early` stays at zero (otherwise raise `num_traces`).
- [ ] All error traces are present in the backend; request-rate dashboards match ingress metrics.

## Checked

2026-10-24. OpenTelemetry Collector contrib tailsamplingprocessor README and documentation.md, probabilisticsamplerprocessor README (main branch), and the OpenTelemetry specification SDK environment variables. Confirmed: tail sampling defaults (`decision_wait` 30s, `num_traces` 50000, `expected_new_traces_per_sec` 0), policy type names and config keys used in the example, decision flow, composite rate allocation, statefulness warning and placement note, metric names, probabilistic sampler modes, `hash_seed` rule, stability levels, `sampling.priority`, tracestate `ot=th:` encoding, and sampler env variable semantics. Removed the Tempo-specific claim.

Method: documentation only; no commands were run.
