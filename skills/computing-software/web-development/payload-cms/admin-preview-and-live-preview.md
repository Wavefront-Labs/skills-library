---
id: computing-software.web-development.payload-cms.admin-preview-and-live-preview
name: admin-preview-and-live-preview
category: computing-software
field: web-development
product: payload-cms
tags: [live-preview, preview-button, draft-preview, iframe-preview]
level: practitioner
status: docs-checked
description: "Enable Live Preview with admin.livePreview (url, collections, globals, breakpoints) and the Preview button with admin.preview."
sources:
  - https://payloadcms.com/docs/live-preview/overview
  - https://payloadcms.com/docs/admin/preview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Live Preview and Preview

Goal: show the frontend next to the editor.

Root config:

```ts
export default buildConfig({
  admin: {
    livePreview: {
      url: 'http://localhost:3000',
      collections: ['pages'],
      breakpoints: [{ label: 'Mobile', name: 'mobile', width: 375, height: 667 }],
    },
  },
})
```

Options: `url` (string or function returning a string, used as the iframe `src`), `breakpoints`, `collections`, `globals`. Dynamic URL:

```ts
url: ({ data, collectionConfig, locale }) => `http://localhost:3000/${data.slug}`
```

A collection or global `admin.livePreview` is merged over the root settings as overrides. A relative `url` is accepted. The `url` function receives `{ data, locale, collectionConfig, globalConfig, req }`.

Preview is different: `admin.preview` on a collection or global returns a link and adds a Preview button to the Edit View, which you can use for Draft Preview:

```ts
admin: { preview: (doc, { locale, req, token }) => doc?.slug ? `http://localhost:3000/${doc.slug}` : null }
```

The `preview` function receives the document and `{ locale, req, token }`; returning `null` hides the Preview button.

## Checked

2026-11-04. Read live-preview/overview and admin/preview in the payloadcms/payload docs. Confirmed: livePreview options, merge of per-entity overrides, url function arguments, preview function arguments. Added: admin/preview as a source, null return behaviour. Removed: the unconfirmed verify step.
Method: documentation only; no commands were run.
