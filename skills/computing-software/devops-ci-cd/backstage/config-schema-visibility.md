---
id: computing-software.devops-ci-cd.backstage.config-schema-visibility
name: config-schema-visibility
category: computing-software
field: devops-ci-cd
product: backstage
tags: [config-schema, visibility, frontend-config, backstage]
level: advanced
status: docs-checked
description: "Define a plugin's config schema in TypeScript or JSON Schema and mark which keys the frontend may read."
sources:
  - https://backstage.io/docs/conf/defining
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Backstage validates configuration against a schema assembled from all packages in the ecosystem. Each package contributes through a top-level `configSchema` field in `package.json`, which holds an inline JSON schema or a relative path to a `.json` or `.d.ts` file. A package counts as part of the ecosystem if it depends on something in the `@backstage` namespace or has a `configSchema` field.

```ts
export interface Config {
  app: {
    /**
     * Frontend root URL
     * @visibility frontend
     */
    baseUrl: string;
    /** @items.visibility frontend */
    myItems: string[];
  };
}
```

```jsonc
{
  "configSchema": "config.d.ts",
  "files": ["dist", "config.d.ts"]
}
```

- Values are backend-only by default. Add `@visibility frontend` to expose a key to the browser, or `@deepVisibility` to apply it to a whole subtree.
- `@visibility secret` keeps a value backend-only and it may be excluded from logs; the levels are `frontend`, `backend` (default) and `secret`.
- Separate `.json` schemas can start with `"$schema": "https://backstage.io/schema/config-v1"`.
- List the schema file in the package's `files` so it is published.

Visibility applies only to the direct parent of where the keyword is placed: marking an object `frontend` without marking its children exposes only an empty object, though ancestors need not declare visibility themselves.

## Checked

2026-11-03. Confirmed against the Backstage Defining Configuration for your Plugin page: `configSchema` in package.json, ecosystem definition, `.json` and `.d.ts` formats, `files` entry, `$schema` URL, visibility levels and annotations. Removed: the unsupported advice on frontend keys and defaults, and the claim that `@secret` is a separate annotation.

Method: documentation only; no commands were run.
