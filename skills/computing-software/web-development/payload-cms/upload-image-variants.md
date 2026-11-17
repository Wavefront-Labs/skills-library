---
id: computing-software.web-development.payload-cms.upload-image-variants
name: upload-image-variants
category: computing-software
field: web-development
product: payload-cms
tags: [image-variants, sharptransformer, image-sizes, transformer-sharp]
level: practitioner
status: docs-checked
description: "Generate resized image variants with sharpTransformer from @payloadcms/transformer-sharp configured under upload.transformers."
sources:
  - https://payloadcms.com/docs/upload/transformers
  - https://payloadcms.com/docs/upload/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Image variants with sharpTransformer

Goal: create thumbnail and card sizes on upload. Install with `pnpm add @payloadcms/transformer-sharp`.

```ts
import { sharpTransformer } from '@payloadcms/transformer-sharp'

export default buildConfig({
  collections: [/* Media collection with upload enabled */],
  upload: {
    transformers: [
      sharpTransformer({
        collections: {
          media: {
            variants: [
              { name: 'thumbnail', width: 400, height: 300, position: 'centre' },
              { name: 'card', width: 768, height: 1024, position: 'centre' },
              { name: 'tablet', width: 1024, height: undefined, position: 'centre' },
            ],
          },
        },
      }),
    ],
  },
})
```

Leaving `height` undefined keeps the aspect ratio. If the upload is smaller than a variant, the variant is null by default; `withoutEnlargement: true` returns the original instead and `false` enlarges it. Payload crops and resizes each upload to every declared variant and the Admin Panel lists each variant's width, height and size.

Rules:

- `upload.transformers` is the only transformer configuration surface; there is no per-collection list.
- Every transformer needs a unique, non-empty `slug`; duplicates fail at startup.
- Registering any transformer routes `/api/<collection>/file/<filename>` through the transformer-aware handler; a file on disk without a matching document returns 404.
- Transformers run in array order and return `continue` or `complete`.
- Setting `variants` or `imageSizes` on the collection's own `upload` config fails the build; they live on `sharpTransformer({ collections })`.
- Request-time resizing (`?width=400`) is off by default; enable it with `sharpTransformer({ dynamic: { collections: ['media'] } })` and read the page's securing advice first.

Verify: after upload, the document shows a `variants` entry for each name.

## Checked

2026-11-04. Read upload/transformers and upload/overview. Confirmed: upload.transformers as the only configuration surface, unique non-empty slugs with a startup error on duplicates, the changed file endpoint and 404 for files without a document, continue and complete ordering, the pnpm install command, sharpTransformer collections variants example, variants stored under variants.<name>, height left undefined keeping aspect ratio, withoutEnlargement behaviour, and dynamic resizing being disabled by default. Added: variant null default, collection-level variants failing the build, and dynamic resizing.
Method: documentation only; no commands were run.
