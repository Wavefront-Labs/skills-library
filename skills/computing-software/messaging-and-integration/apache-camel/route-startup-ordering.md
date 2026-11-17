---
id: computing-software.messaging-and-integration.apache-camel.route-startup-ordering
name: route-startup-ordering
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, routes, startup-order, autostartup, lifecycle]
level: practitioner
status: docs-checked
description: "Camel route startupOrder rules (unique integers, auto-numbering from 1000) and autoStartup at context and route level."
sources:
  - https://camel.apache.org/manual/configuring-route-startup-ordering-and-autostartup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Startup order and autoStartup

**autoStartup**: routes start automatically by default.
- Context: `camel.main.auto-startup = false` (application.properties), `camelContext.setAutoStartup(false)`, or `autoStartup="false"` on `<camelContext>`. Read once at startup.
- Route: `autoStartup(false)` (Java), `autoStartup="false"` (XML), `autoStartup: "false"` (YAML). Java accepts a boolean, a string or a placeholder like `"{{startupRouteProperty}}"`.
- Start later with `camel.getRouteController().startAllRoutes()` (also via JMX, needs camel-management).

**startupOrder**: an Integer per route; lowest starts first.
- Values must be unique in the CamelContext; a duplicate throws `FailedToStartRouteException`.
- Routes without a value are auto-numbered from 1000, so keep your own values below 1000 and use 10000 or more for routes that must start last.
- Gaps are fine (100, 200, 89).
- Example: `seda:foo` order 1 and `direct:start` order 2, so the consumer runs before the sender.

Shutdown uses the reverse of startup order.

Verify: with two routes ordered 1 and 2, the startup log lists route 1 started first; reusing a number fails startup.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read in full the Camel page on route startup ordering and auto-startup. Confirmed: context and route level autoStartup, camel.main.auto-startup, setAutoStartup, startAllRoutes and the JMX route (camel-management), the boolean, string and placeholder forms, startupOrder uniqueness and FailedToStartRouteException, auto-numbering from 1000 with 10000 as a safe high range, gaps allowed, the seda:foo and direct:start example, reverse-order shutdown. The Verify line is generic advice, not a page claim.
