---
id: computing-software.cloud-infrastructure-engineering.datadog.log-pipelines
name: log-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, log-pipelines, processors, grok-parser, log-remapper]
level: practitioner
status: docs-checked
description: "Parse and enrich logs with Datadog log pipelines, the Grok parser, remappers and category/lookup/arithmetic processors, and know which attributes are reserved."
sources: ["https://docs.datadoghq.com/logs/log_configuration/pipelines/", "https://docs.datadoghq.com/logs/log_configuration/parsing/", "https://docs.datadoghq.com/logs/log_configuration/processors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log pipelines and processors
Goal: turn raw log lines into structured attributes.

How it works: each log is tested against every pipeline filter; if it matches, that pipeline's processors run in order before the next pipeline. The pipeline filter is applied before the pipeline's processors, so you cannot filter on an attribute extracted inside the same pipeline. Pipelines can be nested, and can be reordered with the Move to option.

Grok rule examples from the parsing page (matchers `word`, `notSpace`, `number`, `integer`, `data`, `ip`, `date(...)`):

```
MyParsingRule %{word:user} connected on %{date("MM/dd/yyyy"):date}
user %{word:user.name} id:%{integer:user.id}
server on server %{notSpace:server.name} in %{notSpace:server.env}
```

Filters follow the extract: `scale(factor)` multiplies a number, and `number`/`integer` convert types.

- Processors in the processor reference: Grok parser, Log date remapper, Log status remapper, Service remapper, Log message remapper, Trace remapper, Span remapper, Category processor, Lookup processor, Arithmetic processor, String builder, URL parser, User-Agent parser, GeoIP parser and others.
- Recommended limits: at most 20 processors per pipeline and 10 parsing rules in a Grok processor; Datadog may disable under-performing rules, processors or pipelines.
- Integration pipelines are read-only and installed automatically when a log arrives with a matching `source`; they cannot be edited.
- Conflict rules: Grok parser, Category, Arithmetic, String builder, Lookup, URL parser, User-Agent parser, GeoIP and Decoder processors are last-write-wins; Log status remapper, Service remapper, Log message remapper, Trace remapper and Span remapper are first-write-wins (the Log date remapper uses the last one).
- Reserved attributes include `host`, `service`, `status`, `message`, `timestamp` and `trace_id`. For JSON logs, preprocessing maps attributes such as `@timestamp`, `timestamp`, `date` or `eventTime` to the log date; if none is present Datadog uses the time the log was received. Use the date remapper to name a different source attribute.

Gotcha: because first-write-wins processors keep the earliest value, order status, service and message remappers deliberately.

## Verify
- A new log shows the parsed attributes in the side panel, and you can create facets from them.

## Checked
2026-11-03. Confirmed against the Log Pipelines, Parsing and Processors pages. Removed: the draft's `access_rule` Grok example (its `duration:scale(1000000)` unit and standard attribute names were not confirmed), "duration in nanoseconds" claim, and generic ordering advice.
Method: documentation only; no commands were run.
