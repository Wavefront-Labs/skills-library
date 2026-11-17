---
id: computing-software.web-development.payload-cms.query-depth
name: query-depth
category: computing-software
field: web-development
product: payload-cms
tags: [depth, populate-relationships, defaultdepth, maxdepth]
level: practitioner
status: docs-checked
description: "Control relationship and upload population with depth, defaultDepth (1), the root maxDepth and a field-level maxDepth."
sources:
  - https://payloadcms.com/docs/queries/depth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Depth

Goal: choose how deeply relationships are populated.

- `depth: 0` returns related IDs only; `depth: 1` replaces them with the related documents.

```ts
await payload.find({ collection: 'posts', overrideAccess: true, depth: 2 })
```

REST: `fetch('https://localhost:3000/api/posts?depth=2')`.

Defaults: if no depth is given Payload uses `defaultDepth`, which is `1`. Change it in the root config:

```ts
export default buildConfig({ defaultDepth: 2, maxDepth: 5 })
```

Field-level cap that applies regardless of the requested depth:

```ts
{ name: 'author', type: 'relationship', relationTo: 'users', maxDepth: 2 }
```

Depth affects performance and circular relationships could otherwise populate endlessly, so set a root `maxDepth` (default 10) for public APIs. GraphQL does not use `depth` because population follows the shape of the query. `findGlobal` also accepts `depth`.

Verify: compare response sizes at depth 0 and 2.

## Checked

2026-11-04. Read queries/depth and configuration/overview. Confirmed: depth 0 returns IDs and depth 1 populates documents, Local API depth option, REST depth parameter, defaultDepth defaulting to 1, field-level maxDepth, no effect of depth in GraphQL, and findGlobal using depth. The root maxDepth default of 10 is from the config overview table.
Method: documentation only; no commands were run.
