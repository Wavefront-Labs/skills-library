---
id: computing-software.web-development.payload-cms.global-config
name: global-config
category: computing-software
field: web-development
product: payload-cms
tags: [globals, global-config, singleton, site-settings]
level: practitioner
status: docs-checked
description: "Define a Global for single-document content such as navigation or site settings, with its own access, hooks, versions and admin options."
sources:
  - https://payloadcms.com/docs/configuration/globals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Global config

Goal: model a singleton (header nav, site banner) as a Global.

```ts
import type { GlobalConfig } from 'payload'

export const Nav: GlobalConfig = {
  slug: 'nav',
  fields: [
    {
      name: 'items',
      type: 'array',
      required: true,
      maxRows: 8,
      fields: [{ name: 'page', type: 'relationship', relationTo: 'pages', required: true }],
    },
  ],
}
```

Register it with `globals: [Nav]` in the Payload Config.

Options in the docs table: `access`, `admin`, `authorship` (on by default), `custom`, `dbName`, `description`, `endpoints`, `fields` (required), `graphQL`, `hooks`, `label`, `lockDocuments` (on by default), `slug` (required), `typescript`, `versions`, `select`. `admin.group: false` hides the Global from navigation while its routes stay accessible.

- Use a Global only when exactly one document exists; for several items sharing a structure use a Collection.
- Global access control has `read`, `update`, `validate` (and `readVersions` when versions are enabled); there is no create or delete.
- Read it with `payload.findGlobal({ slug: 'nav' })`, update with `payload.updateGlobal`.

The REST path is `/api/globals/{slug}`; GraphQL exposes a query named after the Global and an `update<Name>` mutation.

## Checked

2026-11-04. Read configuration/globals, access-control/globals, local-api/overview, rest-api/overview and graphql/overview in the payloadcms/payload docs. Confirmed: example, option table, read/update/validate/readVersions access, findGlobal and updateGlobal, REST path. Added: lockDocuments, group false, GraphQL naming. Removed: the sidebar verify step.
Method: documentation only; no commands were run.
