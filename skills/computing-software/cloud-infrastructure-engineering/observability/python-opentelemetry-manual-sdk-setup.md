---
id: computing-software.cloud-infrastructure-engineering.observability.python-opentelemetry-manual-sdk-setup
name: python-opentelemetry-manual-sdk-setup
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry, python-otel-sdk-setup, python, otlp-exporter, tracerprovider, meterprovider]
level: practitioner
status: docs-checked
description: "Set up the OpenTelemetry Python SDK by hand: resource, TracerProvider with BatchSpanProcessor, MeterProvider with periodic reader, logging bridge, and fork-safe servers."
sources: ["https://opentelemetry.io/docs/languages/python/instrumentation/", "https://opentelemetry.io/docs/languages/python/exporters/", "https://opentelemetry-python.readthedocs.io/en/latest/sdk/index.html", "https://opentelemetry.io/docs/zero-code/python/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python OpenTelemetry manual SDK setup

**Goal:** explicit, testable telemetry setup in a Python service when not using `opentelemetry-instrument`.

## Install
```bash
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

## telemetry.py
```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider
import logging

def setup(service: str, version: str):
    res = Resource.create({"service.name": service, "service.version": version})   # OTEL_RESOURCE_ATTRIBUTES can supply further attributes
    tp = TracerProvider(resource=res)
    tp.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))                  # endpoint from OTEL_EXPORTER_OTLP_ENDPOINT
    trace.set_tracer_provider(tp)
    reader = PeriodicExportingMetricReader(OTLPMetricExporter())
    metrics.set_meter_provider(MeterProvider(resource=res, metric_readers=[reader]))
    lp = LoggerProvider(resource=res); lp.add_log_record_processor(BatchLogRecordProcessor(log_exporter))  # your OTLP log exporter (see the Python exporters docs)
    set_logger_provider(lp)
    logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=lp))
    return tp
```
Then add the instrumentation library packages for your frameworks (see the Python instrumentation docs).

## Pre-fork servers (gunicorn, uWSGI)
`BatchSpanProcessor` is not fork-safe (its export thread is lost across `fork`). Initialise in the worker:
```python
# gunicorn.conf.py
def post_fork(server, worker):
    from telemetry import setup; setup("orders", "1.4.2")
```

## Shutdown
Shut down the tracer, meter and logger providers on exit, or short-lived scripts lose the last batch.

## Gotchas
- The logs SDK is imported from `_logs` modules, as in the Python docs; pin versions.
- Sampling: the default sampler is `ParentBased(root=AlwaysOn)`; set `OTEL_TRACES_SAMPLER` to change it.

## Verify
- [ ] With `OTEL_EXPORTER_OTLP_ENDPOINT` set, traces, metrics and logs arrive with identical `service.name`; `ConsoleSpanExporter` in a unit test prints spans.

## Checked
- 2026-10-28. Checked against the OpenTelemetry Python instrumentation, exporters and zero-code pages and the opentelemetry-python SDK docs (resources, trace, trace.export, fork-process-model).
- Confirmed: `Resource.create`, `TracerProvider`, `BatchSpanProcessor`, `PeriodicExportingMetricReader`, `MeterProvider(metric_readers=...)`, `set_meter_provider`, `LoggerProvider`/`LoggingHandler`, http OTLP exporter import paths, `OTEL_TRACES_SAMPLER`, default sampler, `post_fork` hook, fork-safety note.
- Fixed: exporter imports switched to the http/protobuf paths shown in the docs. Removed (unconfirmed): grpc metric and log exporter paths, `export_interval_millis`, Flask/Requests instrumentor calls, `service.instance.id` per-worker claim, opentelemetry-instrument double-setup claim, ParentBased/TraceIdRatioBased constructor example.
Method: documentation only; no commands were run.
