---
id: computing-software.cloud-infrastructure-engineering.observability.otel-asynchronous-instruments
name: otel-asynchronous-instruments
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observable-instruments, async-instrument-callback, otel-metrics, opentelemetry-metrics, meter-provider]
level: practitioner
status: docs-checked
description: "Choose between OpenTelemetry asynchronous counter, up-down counter and gauge, and write a Python callback that reports values at collection time and respects its timeout."
sources: ["https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-instrument-api", "https://opentelemetry.io/docs/languages/python/instrumentation/#metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asynchronous (observable) instruments

Asynchronous instruments have callback functions that report measurements. The callbacks are called only when
the Meter is being observed (metric collection), and the order of callback execution is not specified. Use them to
periodically measure a value that cannot be instrumented directly. Synchronous instruments, by contrast, are used
inline with application logic such as handling a request.

## Pick the instrument (OpenTelemetry metrics API spec)
| Instrument | Reports | Spec examples |
|---|---|---|
| Asynchronous Counter (ObservableCounter) | monotonically increasing value(s) | CPU time per thread, process or system; page faults per process |
| Asynchronous UpDownCounter | additive value(s) that may go up or down | process heap size, where summing across processes gives total heap use |
| Asynchronous Gauge | non-additive value(s) | room temperature, which makes no sense to sum across rooms |

Spec cross-references: if an UpDownCounter value only increases, use the Asynchronous Counter; if the value is
non-additive, use the Asynchronous Gauge; if a Gauge value is additive, use an Asynchronous Counter or
UpDownCounter.

## Creating one
The API accepts a name, and optionally a unit, a description, advisory parameters and zero or more callbacks that
are permanently registered on the new instrument. The SHOULD-level spec text also lets callbacks be registered
after creation and undone, where the language API supports it. The spec recommends the idiomatic name
`ObservableCounter` (for example `observable_counter`) where possible.

## Python (opentelemetry.io Python page)
Each callback accepts options from the SDK and returns its observations.
```python
from typing import Iterable
from opentelemetry.metrics import CallbackOptions, Observation

def scrape_config_versions(options: CallbackOptions) -> Iterable[Observation]:
    r = requests.get("http://configserver/version_metadata",
                     timeout=options.timeout_millis / 10**3)
    for metadata in r.json():
        yield Observation(metadata["version_num"], {"config.name": metadata["version_num"]})

meter.create_observable_gauge("config.version", callbacks=[scrape_config_versions],
                              description="The active config version for each configuration")
```
The options passed to the callback contain a timeout. Callbacks should respect it to avoid blocking indefinitely.

## Gotchas
- Because callbacks run during collection, a slow or blocking callback holds up collection; honour the timeout.
- Picking Gauge for an additive value loses the ability to sum across instances meaningfully; the spec points
  additive values to the counter or up-down counter.

## Verify
- [ ] The instrument kind matches the value: monotonic, additive up and down, or non-additive.
- [ ] Callbacks use the timeout from their options.

## Checked
2026-11-09. Confirmed against the OpenTelemetry metrics API specification (asynchronous instrument API,
Asynchronous Counter, Gauge and UpDownCounter sections read) and the opentelemetry.io Python instrumentation
page (metrics section read from its markdown source). Removed the Go example and pkg.go.dev source (not read),
the claims that counter callbacks must return running totals, that exceptions are swallowed, and that missing
attribute sets disappear, and the queue-depth Python example, which were not on those pages.
Method: docs-checked 2026-11-09 against the specification markdown (metrics/api.md) and the opentelemetry.io Python instrumentation markdown source; documentation only, no commands run.
