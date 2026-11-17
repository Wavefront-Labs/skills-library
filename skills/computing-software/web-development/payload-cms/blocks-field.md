---
id: computing-software.web-development.payload-cms.blocks-field
name: blocks-field
category: computing-software
field: web-development
product: payload-cms
tags: [blocks-field, page-builder, blocktype, block-config]
level: practitioner
status: docs-checked
description: "Build flexible layouts with a blocks field whose blocks each have slug, fields, labels and interfaceName."
sources:
  - https://payloadcms.com/docs/fields/blocks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Blocks field

Goal: let editors compose content from different block types.

```ts
{
  name: 'layout',
  type: 'blocks',
  minRows: 1,
  blocks: [
    {
      slug: 'hero',
      interfaceName: 'HeroBlock',
      fields: [{ name: 'heading', type: 'text' }],
    },
    {
      slug: 'cta',
      fields: [{ name: 'label', type: 'text' }, { name: 'url', type: 'text' }],
    },
  ],
}
```

Field options: `name`, `blocks` (required), `minRows`, `maxRows`, `labels`, `validate`, `defaultValue`, `localized`, `unique`, plus admin `initCollapsed`, `isSortable`.

Block options: `slug` (required), `fields` (required), `labels`, `interfaceName`, `graphQL.singularName`, `dbName`, `custom`, `components.Block`, `components.Label`, `admin.disableBlockName`, `admin.group` and `images` for block previews.

Each saved block carries `blockType` (the slug) and optionally `blockName`; the frontend switches on `blockType`.

Block `images` previews use an icon of 20x20 and a 3:2 thumbnail. Gotcha: `unique: true` on a field nested inside a block makes it unique across the whole collection, not per block row.

## Checked

2026-11-04. Read fields/blocks in the payloadcms/payload docs. Confirmed: field and block options, blockType and blockName, components and images. Removed: the slug uniqueness and slug-rename gotcha and the verify step (not on the page). Added: nested unique warning, images sizes.
Method: documentation only; no commands were run.
