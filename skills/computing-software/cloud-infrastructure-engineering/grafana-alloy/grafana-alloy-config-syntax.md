---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-config-syntax
name: grafana-alloy-config-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [alloy-syntax, blocks, attributes, identifiers, comments, terminators]
level: intro
status: docs-checked
description: "Alloy configuration syntax rules for comments, identifiers, attributes, labeled blocks, newline terminators and formatting."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/get-started/syntax.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alloy configuration syntax

The syntax is declarative; order of blocks and attributes does not matter because dependencies are resolved automatically.

- **Comments**: `// single line` and `/* block */`.
- **Identifiers**: letters (Unicode allowed), digits and underscores, not starting with a digit. `my-component`, `my component` and `my.component` are invalid.
- **Attributes**: `NAME = VALUE`, where the value is a constant (string, number, bool, array, object) or an expression (function call, component reference, calculation).
- **Blocks**: `BLOCK_NAME "LABEL" { ... }` with an optional label and a required body. Block names are dot-separated component names (`prometheus.scrape`) or special blocks (`logging`, `tracing`). Labels are double-quoted (never single), valid identifiers, and unique per component type.

```alloy
local.file "api_key" {
  filename  = sys.env("API_KEY_PATH")
  is_secret = true
}
prometheus.remote_write "production" {
  endpoint {
    url = "https://prometheus.example.com/api/v1/write"
  }
  queue_config {
    capacity             = 10000
    max_samples_per_send = 2000
  }
}
```

Every attribute and block must end with a newline (the terminator), which follows a complete expression or `]`, `)`, `}`. Newlines inside multi-line arrays and objects are ignored. Run `alloy fmt` to standardise indentation and validate syntax.

## Checked

2026-11-08. Read the Alloy syntax page (get-started/syntax.md) in full. Confirmed: declarative order independence, both comment styles, identifier rules with the invalid examples, attribute and block forms, block naming and label rules (double-quoted, unique), newline terminators, and the formatter description.

Method: documentation only; no commands were run.
