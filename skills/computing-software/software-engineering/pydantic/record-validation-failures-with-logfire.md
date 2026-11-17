---
id: computing-software.software-engineering.pydantic.record-validation-failures-with-logfire
name: record-validation-failures-with-logfire
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-logfire, logfire, instrument-pydantic, observability, validation-error, scrubbing, production-debugging]
level: practitioner
status: docs-checked
description: "Record failed Pydantic validations in Logfire with instrument_pydantic(record=...), choose the record level, and scrub rejected input values before export."
sources:
  - https://docs.pydantic.dev/latest/integrations/logfire/
  - https://docs.pydantic.dev/latest/errors/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: capture production `ValidationError`s with their structured errors and surrounding trace.

## Setup
Needs a Logfire account and project.
```bash
pip install logfire
logfire auth
```
Call `instrument_pydantic()` before defining or importing the models to monitor:
```python
import logfire
logfire.configure()
logfire.instrument_pydantic(record='failure')
```
Troubleshooting from the page: if no records appear, make sure `logfire.configure()` runs and `instrument_pydantic()` runs before the model class is defined or imported.

## The `record` argument
| Setting | Individual records | Metrics |
|---|---|---|
| `failure` | failed validations only | all validations |
| `all` (default) | every success and failure | all validations |
| `metrics` | none | all validations |
| `off` | none | none |

Use `failure` for production troubleshooting; use `all` in development to inspect successful inputs. `record='all'` creates a span for every validation, so review data volume and privacy before using it in production. With `failure`, successes are metrics only.

## Privacy
Failed-validation records contain the rejected values from the structured errors. Logfire scrubs common sensitive values, but stores every rejected value under the key `input` inside the serialized `errors` attribute. If those values can hold secrets or personal data:
```python
logfire.configure(
    scrubbing=logfire.ScrubbingOptions(extra_patterns=[r'(?:^input$|"input"\s*:)'])
)
```
Alternatively use `record='metrics'` so individual failures are not exported.

## Using the data
- Filter the Live view by `schema_name`, or query the structured `errors` field in SQL, to find models, fields and error types that fail most.
- Logfire alerts run a SQL query on a schedule and notify you (for example in Slack).
- Instrument your web framework, database client or task queue so the failure sits inside the request or job trace.
- Explanations of failed validations are an early-access feature that currently requires "Pydantic validation suggestions" enabled in Logfire and `record='all'`.
- You can attach a model to a log: `logfire.info('user processed: {user!r}', user=user)`.

Per-model settings and environment-variable configuration are in the Logfire Pydantic integration reference.

## Checked

Checked 2026-11-07. Re-read integrations/logfire and errors/troubleshooting in full and compared every claim, including the record table and scrubbing pattern; no changes needed.

Method: documentation only; no commands were run.
