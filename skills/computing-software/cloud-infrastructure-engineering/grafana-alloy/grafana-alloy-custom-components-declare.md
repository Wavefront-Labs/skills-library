---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-custom-components-declare
name: grafana-alloy-custom-components-declare
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [declare, argument, export, custom-components]
level: practitioner
status: docs-checked
description: "Package a pipeline as a reusable Alloy custom component with declare, argument and export blocks, and instantiate it like a built-in."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/get-started/components/custom-components.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/config-blocks/declare.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom components with declare

A custom component bundles arguments, exports and internal components. The label of a `declare` block becomes the component name, and the controller treats it like a built-in: arguments are evaluated and passed in, internal components run, exports update when internal exports change, and health reflects the internals.

Inside `declare` you can use:
- `argument "NAME"`: an input; read it with `argument.NAME.value`. Set `optional = false` to require it and `comment` to document it.
- `export "NAME"`: an output with a `value` expression.
- built-in or other custom components.

```alloy
declare "add" {
  argument "a" {
    comment  = "First number to add"
    optional = false
  }
  argument "b" {
    optional = false
  }
  export "sum" {
    value = argument.a.value + argument.b.value
  }
}

add "example" {
  a = 15
  b = 17
}
// add.example.sum == 32
```

A realistic use wraps `loki.process` with `forward_to = argument.write_to.value` and exports `loki.process.filter.receiver` as `filter_input`, so callers can send logs into the packaged pipeline. Share declared components across files with modules (import.file and friends).

## Checked

2026-11-08. Read the Custom components page and the declare block reference in full. Confirmed: the label becomes the component name, the allowed contents, how the controller treats custom components, `argument.NAME.value`, `optional` and `comment`, the add example, and sharing through modules. The loki.process wrapper description matches the module example on the Modules page.

Method: documentation only; no commands were run.
