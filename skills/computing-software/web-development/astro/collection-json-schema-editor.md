---
id: computing-software.web-development.astro.collection-json-schema-editor
name: collection-json-schema-editor
category: computing-software
field: web-development
product: astro
tags: [json-schema, vscode-settings, yaml-schema, editor-intellisense]
level: practitioner
status: docs-checked
description: "Use the JSON Schema files Astro generates in .astro/collections for IntelliSense in JSON and YAML data files, including VS Code settings."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Astro generates a JSON Schema per collection in `.astro/collections/`, e.g. `.astro/collections/authors.schema.json`.

In a JSON file, point to it with `$schema` (a relative path from the data file):

```json
{
  "$schema": "../../../.astro/collections/authors.schema.json",
  "name": "Armand",
  "skills": ["Astro", "Starlight"]
}
```

For a group of JSON files in VS Code, use the `json.schemas` setting:

```json
{
  "json.schemas": [
    {
      "fileMatch": ["/src/data/authors/**"],
      "url": "./.astro/collections/authors.schema.json"
    }
  ]
}
```

For YAML, install the Red Hat YAML extension and use a comment:

```yaml
# yaml-language-server: $schema=../../../.astro/collections/authors.schema.json
name: Armand
```

Or apply to a group of YAML files with `yaml.schemas`:

```json
{
  "yaml.schemas": {
    "./.astro/collections/authors.schema.json": ["/src/content/authors/*.yml"]
  }
}
```

## Checked

2026-11-04. Confirmed against the Astro content collections guide: .astro/collections output, $schema, json.schemas, the Red Hat YAML comment syntax and yaml.schemas. Nothing removed.

Method: documentation only; no commands were run.
