---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.alloy-configuration-syntax-and-components
name: alloy-configuration-syntax-and-components
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [alloy-syntax, alloy, grafana-alloy, components, blocks, attributes, expressions]
level: practitioner
status: docs-checked
description: "Write Grafana Alloy configuration: blocks, attributes, identifiers, labels, terminators and formatting."
sources: ["https://grafana.com/docs/alloy/latest/get-started/syntax/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read and write Alloy configs that parse correctly.

The syntax is declarative: the parser works out dependencies between elements, so the order of blocks and attributes does not matter.

```
local.file "api_key" {
  filename  = sys.env("API_KEY_PATH")
  is_secret = true
}

prometheus.remote_write "production" {
  endpoint {
    url = "https://prometheus.example.com/api/v1/write"

    basic_auth {
      username = "metrics"
      password = local.file.api_key.content
    }
  }
}

prometheus.scrape "web_servers" {
  targets    = [{ "__address__" = "app:8080" }]
  forward_to = [prometheus.remote_write.production.receiver]
}
```

Rules
- **Attributes** are `ATTRIBUTE_NAME = ATTRIBUTE_VALUE`. Values are constants (strings, numbers, booleans, arrays, objects) or expressions such as function calls and component references. Attributes can be top-level settings, component arguments or settings inside nested blocks.
- **Blocks** have a name (required), an optional label and a body in curly braces holding attributes and nested blocks. Block names are component names (dot-separated, such as `prometheus.scrape` or `local.file`) or special blocks like `logging` and `tracing`.
- **Labels** must be valid identifiers wrapped in double quotes (not single), and unique among blocks of the same type. Several instances of a component need different labels.
- **Identifiers** contain UTF-8 letters, digits or underscores and cannot start with a digit. `my-component`, `my component` and `my.component` are invalid.
- **Terminators**: every block and attribute definition ends with a newline. Newlines elsewhere are ignored, so arrays and objects can span lines.
- **Comments**: `//` single line and `/* */` block.
- References to another component's exports use the form `component_type.label.export`, such as `local.file.api_key.content`.

Formatting: `alloy fmt` standardises indentation and whitespace and validates syntax.

## Checked
Method: docs-checked 2026-11-09 against the Alloy docs Alloy syntax page (raw markdown, read in full). Function lists, validate flags and cycle-handling claims were dropped as unconfirmed.
