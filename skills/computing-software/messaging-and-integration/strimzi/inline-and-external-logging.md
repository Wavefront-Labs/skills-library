---
id: computing-software.messaging-and-integration.strimzi.inline-and-external-logging
name: inline-and-external-logging
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [logging-inline, external-logging, log4j2]
level: practitioner
status: docs-checked
description: "Configure operator and component logging with inline or external log4j2 settings."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Logging configuration

**Goal:** change log levels without restarts, or supply a full log4j2 file.

Strimzi operators and Kafka components use **log4j2**. Levels: `INFO`, `ERROR`, `WARN`, `TRACE`, `DEBUG`, `FATAL`, `OFF`. Unconfigured loggers inherit from parents. `DEBUG` and `TRACE` can produce large output and hurt performance.

Set `spec.logging` using one of two methods.

**Inline:** define loggers directly; best for log level changes.

```yaml
logging:
  type: inline
  loggers:
    rootLogger.level: INFO
```

Changes to inline logging in a resource managed by the Cluster Operator are applied dynamically without a pod restart.

**External:** reference a ConfigMap holding a complete `log4j2.properties`, useful for reusable configuration, filters targeting a cluster, topic or operator, and custom appenders.

```yaml
logging:
  type: external
  valueFrom:
    configMapKeyRef:
      name: my-config-map
      key: log4j2.properties
```

Both `name` and `key` are mandatory. The Cluster Operator detects changes to the referenced ConfigMap and applies them dynamically.

**Checklist**

1. Use inline for level tweaks.
2. Use external for filters and appenders.
3. Revert `DEBUG` or `TRACE` after troubleshooting.

## Checked

2026-11-03. Confirmed in the Logging section: inline vs external methods, dynamic application of inline changes without pod restart, mandatory name and key for configMapKeyRef, and the DEBUG/TRACE performance warning.

Method: documentation only; no commands were run.
