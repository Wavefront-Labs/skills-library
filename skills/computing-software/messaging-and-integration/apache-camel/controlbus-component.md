---
id: computing-software.messaging-and-integration.apache-camel.controlbus-component
name: controlbus-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, controlbus, route-control, management]
level: practitioner
status: docs-checked
description: "Camel controlbus component: route actions start, stop, restart, suspend, resume, fail, status, stats, the language command and defaults."
sources:
  - https://camel.apache.org/components/next/controlbus-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# controlbus:

Producer only: `controlbus:command[?options]` with command `route` or `language`.

**route** uses `routeId` and `action`:
- `start`, `stop`, `restart` (waits `restartDelay` between stop and start)
- `suspend`, `resume`
- `fail`: stop and mark failed by exception
- `status`: body gets the status (Started, Stopped...)
- `stats`: body gets XML statistics; needs JMX (on by default); omit `routeId` for the whole CamelContext
- `routeId=current` means the current route

**language** (`controlbus:language:simple`, also groovy, spel, xpath): evaluates the body as an expression and the result replaces the body.

Options (defaults): `async` false (results not set on the Exchange), `restartDelay` 1000 ms, `loggingLevel` INFO, `lazyStartProducer` false.

```java
template.sendBody("controlbus:route?routeId=foo&action=start", null);
```
Patterns: a timer route that starts `foo` five seconds after startup; a watchdog that reads `foo` status every minute and restarts it when Stopped; a timer that writes stats to a file.

Simple: `${camelContext.getRouteController().stopRoute('myRoute')}`. To shut down Camel use `${camelContext.stop()}` with `async=true`, so Camel is not stopped while the message is still being processed.

Verify: `action=status` returns `Started` for a running route.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read in full the Camel Control Bus component page. Confirmed: producer only, commands route and language, all route actions and their meaning, routeId=current, stats as XML needing JMX (enabled by default) and whole-context stats without routeId, language values, option defaults (async false, restartDelay 1000, loggingLevel INFO, lazyStartProducer false), the start, watchdog and stats route patterns, and the Simple stopRoute and camelContext.stop() with async=true examples.
