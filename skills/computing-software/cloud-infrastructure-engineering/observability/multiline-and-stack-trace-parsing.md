---
id: computing-software.cloud-infrastructure-engineering.observability.multiline-and-stack-trace-parsing
name: multiline-and-stack-trace-parsing
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [stack-trace-parsing, multiline-parsing, structured-logging, log-parsing, loki-ingest]
level: practitioner
status: draft
description: "Keep stack traces as one log record: multiline rules in Alloy, Promtail, Fluent Bit, OTel filelog and Vector, with first-line regexes for Java, Python and Go."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/loki/loki.process/#stagemultiline", "https://docs.fluentbit.io/manual/pipeline/filters/multiline-stacktrace", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multiline and stack-trace parsing

Best fix: log JSON so the stack trace is a single escaped string field (`exception.stacktrace`). When you
cannot, join continuation lines at the collector **before** any parsing.

## Pattern: match the first line of each record
Usually a timestamp or level at the start of line.
- Generic timestamp: `^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}`
- Java continuation lines start with whitespace + `at `, `Caused by:`, `...`.
- Python: traceback starts `Traceback (most recent call last):` and the record starts with the log prefix.

## Alloy / Promtail
```alloy
loki.process "java" {
  stage.multiline {
    firstline     = "^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}"
    max_wait_time = "3s"
    max_lines     = 500
  }
  forward_to = [loki.write.default.receiver]
}
```
Promtail: `pipeline_stages: [{multiline: {firstline: '...', max_wait_time: 3s}}]`.
On Kubernetes, put `stage.cri {}` (or `docker {}`) **before** multiline so the CRI prefix is removed first.

## OTel filelog receiver
```yaml
receivers:
  filelog:
    include: [/var/log/app/*.log]
    multiline:
      line_start_pattern: '^\d{4}-\d{2}-\d{2}'
    # or line_end_pattern
```
For container logs the `container` operator handles CRI partial lines (`P` flag); multiline goes after it via
a `recombine` operator: `{type: recombine, combine_field: body, is_first_entry: 'body matches "^\\d{4}"', source_identifier: attributes["log.file.path"]}`.

## Fluent Bit
```
[INPUT]
    Name tail
    Path /var/log/containers/*.log
    multiline.parser docker, cri
[FILTER]
    Name multiline
    Match kube.*
    multiline.key_content log
    multiline.parser java, python, go
```
Built-in parsers `java`, `python`, `go`, `ruby` recognise standard stack traces.

## Gotchas
- `max_wait_time` too short splits traces under low traffic; too long delays logs.
- Each source file/stream must be grouped separately (source_identifier) or interleaved pods merge.
- Docker json-file splits lines >16 KB into partials - handle partial reassembly first.

## Verify
Throw a test exception; in Loki/Explore it appears as one entry with the full trace.
