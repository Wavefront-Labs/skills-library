---
id: computing-software.cloud-infrastructure-engineering.observability.log-sampling-strategies
name: log-sampling-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [log-sampling-strategy, tail-based-log-sampling, reduce-log-volume, structured-logging, otel-collector, logging]
level: practitioner
status: draft
description: "Sample logs safely: keep all errors, rate-limit repetitive lines, sample by trace id so kept logs match kept traces, and record the sample rate."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/probabilisticsamplerprocessor", "https://pkg.go.dev/go.uber.org/zap#SamplingConfig", "https://vector.dev/docs/reference/configuration/transforms/sample/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log sampling strategies

Never sample errors, security or audit events. Sample high-volume success and debug paths.

## Strategies
| Strategy | How | When |
|---|---|---|
| Level-based | keep WARN+ always, sample INFO/DEBUG | default for request logs |
| Rate-limited per message | first N per interval per message key, then 1 in M | log storms, retry loops |
| Trace-consistent | keep a log if its trace_id hashes under the rate | so logs line up with sampled traces |
| Tail (buffered) | buffer per request, flush all only if the request failed/slow | best signal, needs memory per request |

## Implementation
zap (Go) per-message rate limit in the logger:
```go
cfg := zap.NewProductionConfig()
cfg.Sampling = &zap.SamplingConfig{Initial: 100, Thereafter: 100} // per second per message: first 100, then 1/100
```
OTel Collector, trace-consistent sampling of logs:
```yaml
processors:
  probabilistic_sampler/logs:
    sampling_percentage: 10
    attribute_source: traceID     # hashes trace_id so logs match traces sampled at the same rate
  filter/keep-errors: {}          # route errors through a separate unsampled pipeline
```
Use a routing connector to split `severity_number >= SEVERITY_NUMBER_WARN` into an unsampled pipeline and sample the rest.

Vector `sample` transform: `rate: 10`, `key_field: trace_id`, `exclude: '.level == "error"'`.

## Record the rate
Add `sample_rate=10` to sampled records so counts can be re-scaled (`count_over_time(...) * 10`). Better: derive counts as metrics before sampling.

## Gotchas
- Sampling before log-derived metrics or alerts makes them wrong; compute those first.
- Random (non-keyed) sampling breaks multi-line request stories; key by trace or request id.
- Rate limits keyed on the formatted message do nothing if the message includes ids; key on the template/event name.

## Verify
- [ ] Error and audit log counts are identical before and after sampling.
- [ ] Log volume dropped by the expected factor in ingest metrics.
