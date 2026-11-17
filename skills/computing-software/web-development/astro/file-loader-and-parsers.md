---
id: computing-software.web-development.astro.file-loader-and-parsers
name: file-loader-and-parsers
category: computing-software
field: web-development
product: astro
tags: [file-loader, csv-parser, nested-json, collection-ids]
level: practitioner
status: docs-checked
description: "Load many entries from one JSON, YAML or TOML file with file(), supply ids, and add a custom parser for CSV or nested JSON documents."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`file()` loads multiple entries from a single local file. It detects a single array of objects from JSON and YAML, and treats each top-level table as an entry in TOML.

```ts title="src/content.config.ts"
import { defineCollection } from "astro:content";
import { file } from "astro/loaders";

const dogs = defineCollection({
  loader: file("src/data/dogs.json"),
});

export const collections = { dogs };
```

Unlike `glob()`, `file()` does not generate ids: each entry needs a unique `id`, either as a property in an array or as the key in object form.

```json
[
  { "id": "poodle", "coat": "curly", "shedding": "low" },
  { "id": "afghan", "coat": "short", "shedding": "low" }
]
```

```json
{
  "poodle": { "coat": "curly", "shedding": "low" },
  "afghan": { "coat": "silky", "shedding": "low" }
}
```

For unsupported types such as `.csv`, pass a `parser` function (can be async):

```typescript
import { parse as parseCsv } from "csv-parse/sync";

const cats = defineCollection({
  loader: file("src/data/cats.csv", {
    parser: (text) => parseCsv(text, { columns: true, skipEmptyLines: true }),
  }),
});
```

For a nested JSON document holding several collections, use a parser per collection:

```typescript
const dogs = defineCollection({
  loader: file("src/data/pets.json", { parser: (text) => JSON.parse(text).dogs })
});
```

## Checked

2026-11-04. Confirmed against the Astro content collections guide: file() format detection, id requirement, CSV parser and nested JSON parser. Nothing removed.

Method: documentation only; no commands were run.
