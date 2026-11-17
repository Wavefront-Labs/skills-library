---
id: computing-software.cloud-infrastructure-engineering.observability.opentelemetry-instrument-and-python-distros
name: opentelemetry-instrument-and-python-distros
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry-instrument-usage, python-distro, python-instrumentation-libraries, language-instrumentation, zero-code-instrumentation]
level: practitioner
status: docs-checked
description: "Instrument Python with opentelemetry-instrument: distro and bootstrap, CLI flags vs env, disabling libraries, gunicorn/uWSGI pre-fork fixes, and building a custom distro."
sources: ["https://opentelemetry.io/docs/zero-code/python/", "https://opentelemetry.io/docs/zero-code/python/configuration/", "https://opentelemetry-python.readthedocs.io/en/latest/examples/fork-process-model/README.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opentelemetry-instrument and Python distros

## Install
```bash
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install        # installs opentelemetry-instrumentation-* for libs found in the env
# or: opentelemetry-bootstrap -a requirements >> requirements-otel.txt  (pin in builds)
```
Run bootstrap at build time in the image, never at container start.

## Run
```bash
OTEL_SERVICE_NAME=orders \
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-agent:4318 OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
OTEL_TRACES_EXPORTER=otlp OTEL_METRICS_EXPORTER=otlp OTEL_LOGS_EXPORTER=otlp \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
opentelemetry-instrument python app.py
```
CLI flags mirror env: `--service_name orders --traces_exporter console`.

## Selecting libraries
- `OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=redis,urllib3`
- `OTEL_PYTHON_EXCLUDED_URLS="healthz,metrics"`
- Library versions must fall in each instrumentation's supported range; check with `OTEL_LOG_LEVEL=debug`.

## Pre-fork servers (gunicorn, uWSGI)
`BatchSpanProcessor` runs a background export thread that is not fork-safe, so pre-fork workers can fail to export. Fix: initialise the SDK in each
worker, not the master.
```python
# gunicorn.conf.py
def post_fork(server, worker):
    from opentelemetry.instrumentation.auto_instrumentation import initialize
    initialize()
```
The fork-process-model example covers Gunicorn and uWSGI.

## Custom distro
`opentelemetry-distro` is the package that supplies defaults for `opentelemetry-instrument`. To ship team defaults, package your own
distro (see the opentelemetry-python distro and configurator docs for the entry-point names).

## Verify
`OTEL_TRACES_EXPORTER=console opentelemetry-instrument python app.py`, hit an endpoint, see a server span with
`http.route`.

## Checked
- 2026-10-28. Checked against the OpenTelemetry Python zero-code docs (configuration, operator Python page) and the opentelemetry-python fork-process-model example.
- Confirmed: `opentelemetry-bootstrap -a install`, `OTEL_PYTHON_DISABLED_INSTRUMENTATIONS`, `OTEL_PYTHON_EXCLUDED_URLS`, `OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED`, `--service_name`/`--traces_exporter` flags, Gunicorn `post_fork` hook, BatchSpanProcessor fork behaviour.
- Removed (unconfirmed): Django excluded-URLs variable, HTTP header capture variable, `--preload`, uWSGI `@postfork`, `use_reloader`, distro entry-point names.
Method: documentation only; no commands were run.
