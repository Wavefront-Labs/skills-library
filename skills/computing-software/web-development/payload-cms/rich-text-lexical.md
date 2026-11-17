---
id: computing-software.web-development.payload-cms.rich-text-lexical
name: rich-text-lexical
category: computing-software
field: web-development
product: payload-cms
tags: [rich-text, lexical, richtext-field, editor-config]
level: practitioner
status: docs-checked
description: "Set up the Lexical rich text editor globally or per field and extend it with features."
sources:
  - https://payloadcms.com/docs/rich-text/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rich text with Lexical

Goal: enable the rich text editor.

```bash
pnpm install @payloadcms/richtext-lexical
```

Global editor:

```ts
import { lexicalEditor } from '@payloadcms/richtext-lexical'
export default buildConfig({ editor: lexicalEditor({}) })
```

Per field override:

```ts
{ name: 'content', type: 'richText', editor: lexicalEditor({}) }
```

The editor is built on Meta's Lexical and extended through "features", the building blocks that add toolbar buttons, slash-menu items, nodes and behaviours. Defaults cover common formatting; you can add, remove or replace features, and write custom ones (see the custom-features page). Related pages cover blocks inside rich text, converters (JSX, HTML, Markdown, plaintext), rendering on demand and custom views.

Gotcha: pass `lexicalEditor` to the root config; a `richText` field's own `editor` option customises or overrides it. Custom lexical features can be given with `features: ({ defaultFeatures }) => [...]`.

Verify: a richText field shows the toolbar in the Admin Panel.

## Checked

2026-11-04. Read rich-text/overview and fields/rich-text. Confirmed: pnpm install @payloadcms/richtext-lexical, lexicalEditor at the root and per field, Lexical as Meta's framework, features as the extension mechanism with defaultFeatures and rootFeatures, and the existence of pages for blocks, converters (HTML, JSX, Markdown, plaintext), rendering on demand, views and custom features. Removed: the claim that the root editor is required for any richText field (not on the pages read).
Method: documentation only; no commands were run.
