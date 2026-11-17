---
id: computing-software.data-engineering.kestra.polling-trigger
name: polling-trigger
category: computing-software
field: data-engineering
product: kestra
tags: [polling, interval, trigger-rows, jdbc-trigger, when]
level: practitioner
status: docs-checked
description: "Use Kestra polling triggers to start flows when new data appears in a database, queue, storage or FTP system, with interval and when filtering."
sources:
  - https://kestra.io/docs/workflow-components/triggers/polling-trigger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Polling triggers repeatedly check an external system at a fixed `interval` (for example `"PT5M"`) and start a new flow execution when new data or events are detected.

The polling results are available to the flow through the `trigger` variable, such as `{{ trigger.rows }}`. Like all triggers, a polling trigger supports a `when` Pebble expression: when set, the trigger only creates an execution if `when` evaluates to true after new data is detected.

```yaml
triggers:
  - id: watch
    type: io.kestra.plugin.jdbc.postgresql.Trigger
    url: myurl
    interval: "PT5M"
    sql: "SELECT * FROM my_table"
```

Here `url: myurl` is a placeholder; supply a real connection.

Kestra provides polling triggers for databases, message queues, cloud storage and FTP servers. The script plugins for Python, Shell and JavaScript each provide `ScriptTrigger` and `CommandsTrigger` variants that run code or commands on an interval and emit only when a condition matches. Browse the plugin catalog filtered by Trigger.

In Enterprise Edition, polling triggers can be assigned to a specific Worker Queue using `workerSelector.tags`.

## Checked

2026-11-04. Confirmed against the Kestra docs page "Trigger Flows When External Systems Change State" (workflow-components/triggers/polling-trigger): interval property, `trigger` variable, `when` behaviour, PostgreSQL example, script trigger variants, Enterprise `workerSelector.tags`. Removed: "ISO 8601" wording and an invented numbered lifecycle not on the page.
Method: documentation only; no commands were run.
