---
id: computing-software.web-development.strapi.preview-config
name: preview-config
category: computing-software
field: web-development
product: strapi
tags: [strapi, preview, allowedorigins, handler, config-admin, draft-mode]
level: advanced
status: docs-checked
description: "Configure Strapi Preview in config/admin: enabled flag, allowedOrigins, and a handler that builds the front-end preview URL."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/preview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Preview

Configured in the `preview` object of `config/admin`, with three parts.

```javascript
preview: {
  enabled: true,
  config: {
    allowedOrigins: env("CLIENT_URL"),  // Usually your frontend application URL
    async handler(uid, { documentId, locale, status }) {
      const document = await strapi.documents(uid).findOne({ documentId });
      const pathname = getPreviewPathname(uid, { locale, document });

      return `${env('PREVIEW_URL')}${pathname}`
    },
  }
}
```

- `enabled`: activation flag.
- `allowedOrigins`: domains allowed to access previews.
- `handler`: gets the content-type `uid` (e.g. `api::article.article`) and `{ documentId, locale, status }` and returns the URL. `getPreviewPathname` is your own helper (the page builds one in its guide).

## Previewing drafts
The front end's strategy is framework-specific. Three patterns the page lists: a query parameter (`/your-path?preview=true`, as in Nuxt), a dedicated route (`/preview?path=your-path`, as in Next's draft mode), or a different domain (`preview.mysite.com/your-path`).

With Draft & Publish on, branch in the handler on `status`:

```javascript
async handler(uid, { documentId, locale, status }) {
   const document = await strapi.documents(uid).findOne({ documentId });
   const pathname = getPreviewPathname(uid, { locale, document });
   if (status === 'published')  {
      // return the published version
   }
   // return the draft version
},
```

## Checked

Checked 2026-11-04 against the Strapi Preview page (configuration components, previewing drafts, handler examples). Removed the note about the component `info.preview` image, which the page does not mention.

Method: documentation only; no commands were run.
