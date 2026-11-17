---
id: computing-software.messaging-and-integration.apache-camel.message-history
name: message-history
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, message-history, troubleshooting, source-location]
level: practitioner
status: docs-checked
description: "Camel Message History: enabling globally or per route, the MESSAGE_HISTORY property, source location, error handler table and format options."
sources:
  - https://camel.apache.org/components/next/eips/message-history.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message History

Disabled by default; enabling adds small overhead (history lives in a thread-safe list).

Enable:
- Java: `camelContext.setMessageHistory(true)`
- Spring XML: `<camelContext messageHistory="true">`
- application.properties: `camel.main.messageHistory = true` (Spring Boot `camel.main.message-history`, Quarkus `camel.quarkus.message-history`)
- Per route: `.messageHistory()` or `messageHistory="true"` on `<route>`; `messageHistory(false)` turns it off; route level overrides global.

Stored as `org.apache.camel.MessageHistory` entries in an Exchange property (`Exchange.MESSAGE_HISTORY`), not a header. Each entry has route id, processor id, timestamp and elapsed time; `getNode().getId()` gives the node id and `getBodyType()` the body type.

Source locations: `camelContext.setSourceLocationEnabled(true)` or `camel.main.source-location-enabled = true` adds file and line per EIP.

When the error handler logs an exhausted exception with history on, it prints a table with columns Source, ID, Processor and Elapsed (ms) plus a stack trace; with history off it shows only the first step and the failing step. Bodies are not logged by default (`logExhaustedMessageBody(true)` changes that); `logExhaustedMessageHistory(false)` hides the table.

Custom format: global options `CamelMessageHistoryHeaderFormat` and `CamelMessageHistoryOutputFormat` as `String.format` patterns (`camel.main.global-options[...]`).

Verify: a failing route logs the history table listing each step up to the failure.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://camel.apache.org/components/next/eips/message-history.html. No commands were run.
