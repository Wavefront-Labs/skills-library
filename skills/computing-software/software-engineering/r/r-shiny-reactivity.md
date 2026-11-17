---
id: computing-software.software-engineering.r.r-shiny-reactivity
name: r-shiny-reactivity
category: computing-software
field: software-engineering
product: r
tags: [r, r-shiny, shiny-reactivity]
level: advanced
status: draft
description: "Structure Shiny apps with reactive(), observeEvent, isolate and modules, avoiding reactive spaghetti."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reactive expressions, observers and modules
- `reactive()` caches and is lazy; `observeEvent(input$go, {...})` runs side effects; `eventReactive` computes on a trigger.
- Reactive values are only readable in a reactive context; `isolate()` reads without a dependency.
- Modules: `moduleServer(id, function(input, output, session) {...})` with `NS(id)` for UI ids.
- `req()` guards missing inputs; `bindCache()` caches outputs; `promises` and `future` for async.
- Test with `shiny::testServer()`.
Verify: `reactlog::reactlog_enable()` to inspect dependencies.
