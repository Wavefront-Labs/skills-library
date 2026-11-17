---
id: computing-software.database-administration.supabase.storage-buckets-public-private
name: storage-buckets-public-private
category: computing-software
field: database-administration
product: supabase
tags: [storage, buckets, public-bucket, private-bucket, rls]
level: intro
status: docs-checked
description: "Choose between public and private Supabase Storage buckets: default privacy, what RLS still governs, bucket-level restrictions and caching."
sources:
  - https://supabase.com/docs/guides/storage/buckets/fundamentals
  - https://supabase.com/docs/guides/storage/serving/downloads
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide how a bucket's assets are served and protected.

Buckets organise files and set the access model. Upload restrictions, such as maximum file size and allowed content types, are defined at the bucket level.

Private buckets (the default): every operation, including downloads, is subject to RLS policies on `storage.objects`. Files are reachable only two ways:
- A download with an `Authorization` header carrying the user's JWT, checked against the RLS policy.
- A signed URL from `createSignedUrl`, valid for a limited time.
- Authenticated URL form: `https://[project_id].supabase.co/storage/v1/object/authenticated/[bucket]/[asset-name]` (with the Authorization header).
Use for sensitive documents and fine-grained control.

Public buckets: retrieval and serving skip access control, so anyone with the URL can open the file. Uploading, deleting, moving and copying remain governed by RLS. They suit profile pictures, public media and blog content, and perform better because they are cached differently.

```
https://[project_id].supabase.co/storage/v1/object/public/[bucket]/[asset-name]
```

```js
const { data } = supabase.storage.from('bucket').getPublicUrl('filePath.jpg')
console.log(data.publicUrl)
```

Append `?download` to make browsers download instead of display; `?download=customname.jpg` sets the filename.

## Checked

Confirmed against the buckets fundamentals and downloads pages: private by default, RLS on all operations, the two ways to read private files, public bucket behaviour and which operations stay under RLS, example use cases, caching difference, public and authenticated URL forms, getPublicUrl, ?download. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/storage/buckets/fundamentals and guides/storage/serving/downloads (apps/docs/content on GitHub master), read in full.
