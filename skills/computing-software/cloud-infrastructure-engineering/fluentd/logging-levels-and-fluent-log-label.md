---
id: computing-software.cloud-infrastructure-engineering.fluentd.logging-levels-and-fluent-log-label
name: logging-levels-and-fluent-log-label
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, logging, log-level, fluent-log, per-plugin-log, verbosity]
level: practitioner
status: docs-checked
description: "Set global and per-plugin Fluentd log levels and route Fluentd's own logs through the @FLUENT_LOG label to monitoring or a forward aggregator."
sources:
  - https://docs.fluentd.org/deployment/logging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd log levels and capturing logs
Levels, increasing verbosity: `fatal`, `error`, `warn`, `info` (default), `debug`, `trace`.

Global level: `-v` (debug), `-vv` (trace), `-q` (warn), `-qq` (error), or `log_level error` in `<system>`. Per plugin: `@log_level debug` inside a `<source>`, `<match>` or `<filter>`; plugins without it use the global level.

```
<source>
  @type tail
  @log_level debug
</source>
<source>
  @type http
  @log_level fatal
</source>
```
**Capture Fluentd logs**: Fluentd tags its own logs `fluent.<level>` (for example `fluent.info`). Define `<label @FLUENT_LOG>` and match `fluent.*` to process them.

```
<label @FLUENT_LOG>
  <filter fluent.*>
    @type record_transformer
    <record>
      host "#{Socket.gethostname}"
    </record>
  </filter>
  <match fluent.*>
    @type stdout
  </match>
</label>
```
Replace stdout with a monitoring plugin (the page names datadog, sentry, irc), or with `out_forward` to an aggregation server; to capture only errors match `fluent.error`. Add `original_tag ${tag}` to keep the level for downstream filtering.

## Checked

2026-11-04. Confirmed against the Fluentd Logging page (docs.fluentd.org/deployment/logging): level list and default, -v/-vv/-q/-qq, log_level in system, per-plugin @log_level, Capture Fluentd logs section and both cases. Removed: the claim that stacktraces are not routed to @FLUENT_LOG (not on the page).

Method: documentation only; no commands were run.
