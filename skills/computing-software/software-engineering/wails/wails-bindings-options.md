---
id: computing-software.software-engineering.wails.wails-bindings-options
name: wails-bindings-options
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, bindings, options, enums]
level: practitioner
status: docs-checked
description: "Bind Go structs and enums to the Wails frontend with Bind and EnumBind, and shape JS-visible errors with ErrorFormatter."
sources: [https://wails.io/docs/reference/options]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails binding options

Goal: expose Go values to the frontend through `options.App`.

## Method

```go
Bind: []interface{}{
    app,
},
EnumBind: []interface{}{
    AllWeekdays,
},
ErrorFormatter: func(err error) any { return err.Error() },
```

- `Bind` (`[]interface{}`): struct instances whose methods are bound to the frontend.
- `EnumBind` (`[]interface{}`): slices of enum values that should be bound to the frontend (the example passes `AllWeekdays`).
- `ErrorFormatter` (`func(error) any`): decides how an error returned by a JS-to-Go method call is formatted. The returned value is marshalled as JSON, so you can return a structured value instead of a string.
- `BindingsAllowedOrigins` (string): extra allowed origins for the bindings, comma separated, with `*` hostname wildcards.

## Notes

The page documents these only as option fields; it does not describe the generated JavaScript, enum declaration conventions or what the frontend receives for a custom formatter value beyond JSON marshalling.

Related: `computing-software.software-engineering.wails.wails-webview-security-and-context-menu`.

## Gaps

Details of how enums must be declared in Go are not on this page.

## Checked

2026-11-07. Read the whole Options reference page (website/docs/reference/options.mdx), focusing on Bind, EnumBind, ErrorFormatter (JSON-marshalled return value) and BindingsAllowedOrigins (comma-separated, hostname wildcards). The page documents only these option fields, as the skill's own Notes and Gaps sections already say. No claims were trimmed.

Method: documentation only; no commands were run.
