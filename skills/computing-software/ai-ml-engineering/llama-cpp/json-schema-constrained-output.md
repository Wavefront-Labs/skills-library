---
id: computing-software.ai-ml-engineering.llama-cpp.json-schema-constrained-output
name: json-schema-constrained-output
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, json-schema, structured-output, response-format, schema-limits]
level: practitioner
status: docs-checked
description: "Constrain output to a JSON schema and know which schema features the converter does not support."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md", "https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JSON schema output

llama.cpp converts a subset of JSON Schema to a GBNF grammar. Ways to supply a schema:

- llama-cli and llama-completion: `-j, --json-schema SCHEMA`; the server README also lists `-jf, --json-schema-file FILE`.
- llama-server completion endpoints: the `json_schema` body field (for example `{"items": {"type": "string"}, "minItems": 10, "maxItems": 100}`, or `{}` for any JSON).
- llama-server `/chat/completions`: inside `response_format`, for example `{"type": "json_object", "schema": {...}}` or `{"type": "json_schema", "json_schema": {"schema": ...}}`.

Example from the guide (shortened):

```bash
llama-cli -hfr bartowski/Phi-3-medium-128k-instruct-GGUF -hff Phi-3-medium-128k-instruct-Q8_0.gguf \
  -j '{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"age":{"type":"integer"}},"required":["name","age"],"additionalProperties":false}}' \
  -p 'Generate a {name, age}[] JSON array with famous actors of all ages.'
```

The schema only constrains output and is not injected into the prompt, so describe the expected structure in your prompt (tool calling is different: there the schemas are injected).

Known limitations listed on the page:

- `additionalProperties` defaults to false (faster grammars, fewer hallucinations); set `"additionalProperties": true` to allow extra keys, which may then produce keys with unescaped newlines.
- Unsupported features are skipped silently. The guide advises the command-line Python converter to see warnings and `llama-gbnf-validator` to test the grammar.
- Cannot mix `properties` with `anyOf`/`oneOf` in the same type; `prefixItems` is broken (`items` works); nested `$ref`s are broken; remote `$ref`s are unsupported in the C++ version.
- `minimum`, `exclusiveMinimum`, `maximum`, `exclusiveMaximum` only for `"type": "integer"`, not number.
- `pattern` must start with `^` and end with `$`; string formats lack `uri` and `email`; no `patternProperties`.
- Unlikely to be implemented: `uniqueItems`, `contains`/`minContains`, `$anchor`, `not`, and conditionals `if`/`then`/`else`/`dependentSchemas`.

Zod note from the page: `zod-to-json-schema` always sets `additionalProperties: false`.

## Checked

Date: 2026-11-08. Confirmed against the GBNF guide (JSON Schemas to GBNF section) and the llama-server README (`json_schema`, `-j`, `-jf`). Corrected the `response_format` nesting; removed the `examples/json_schema_to_grammar.py` path (the page only says "command-line Python converter") and the unsourced closing sentence.

Method: docs-only read of cited pages, 2026-11-08
