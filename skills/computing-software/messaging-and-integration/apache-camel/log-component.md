---
id: computing-software.messaging-and-integration.apache-camel.log-component
name: log-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, log, slf4j, throughput, show-options]
level: intro
status: docs-checked
description: "Camel log component: log:loggerName URI, level default INFO, showBody and showHeaders defaults, showAll, multiline, maxChars 10000, groupSize throughput logging and logMask."
sources:
  - https://camel.apache.org/components/next/log-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# log:

Producer only; logs through SLF4J. `log:loggerName[?options]`. If the Registry holds a single `org.slf4j.Logger` Camel uses it; `?logger=#myLogger` picks one explicitly; otherwise a logger is made from the category name. Setting `groupSize` switches to the Throughput logger.

Options (defaults):
- `level` INFO (TRACE, DEBUG, INFO, WARN, ERROR, OFF)
- `showBody` true, `showBodyType` true
- `showHeaders` false, `showProperties` false, `showAllProperties` false
- `showExchangeId` false
- `showException`, `showCaughtException`, `showStackTrace` false
- `showStreams` false, `showCachedStreams` true
- `showAll` false (does not set `multiline` or `maxChars`)
- `multiline` false
- `maxChars` 10000
- `skipBodyLineSeparator` true
- `plain` false (body only)
- `style` Default (Tab, Fixed)
- `logMask` false (mask passwords)
- `marker` SLF4J Marker
- `sourceLocationLoggerName` false
- `groupSize`, `groupInterval`, `groupDelay`, `groupActiveOnly` (true)
- `exchangeFormatter` custom

Body in and out is unchanged (any type).

Example: `log:orders?level=WARN&showHeaders=true&multiline=true`.

Verify: the example prints headers on separate lines at WARN.

## Checked

Method: docs-checked 2026-11-09 against https://camel.apache.org/components/next/log-component.html
