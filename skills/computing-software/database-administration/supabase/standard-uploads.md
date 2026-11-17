---
id: computing-software.database-administration.supabase.standard-uploads
name: standard-uploads
category: computing-software
field: database-administration
product: supabase
tags: [storage, uploads, upsert, content-type, rest-upload]
level: intro
status: docs-checked
description: "Standard Supabase Storage uploads: JS call, 6MB guidance, upsert and Asset Already Exists, content type inference and the REST endpoint."
sources:
  - https://supabase.com/docs/guides/storage/uploads/standard-uploads
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: upload small files with one request.

Standard upload suits files up to 6MB. It technically allows up to 5GB, but TUS resumable upload is recommended above 6MB.

```js
const supabase = createClient('your_project_url', 'your_supabase_api_key')
const { data, error } = await supabase.storage.from('bucket_name').upload('file_path', file)
```

Overwriting: uploading to an existing path returns a 400 "Asset Already Exists" error. Pass `{ upsert: true }` in JavaScript or the `x-upsert: true` header with cURL. Overwriting is discouraged because CDN propagation can serve stale content; upload to a new path instead.

Content type: Storage infers it from the file extension. Override with `{ contentType: 'image/jpeg' }` in JavaScript or a `Content-Type` header with cURL. In C# set `inferContentType: false` when specifying it explicitly.

Concurrency: when several clients upload to one path, the first to finish succeeds and the rest get 400 "Asset Already Exists". With `x-upsert`, the last to finish succeeds.

cURL:

```
POST https://{your_project_ref}.supabase.co/storage/v1/object/{bucket_name}/{file_path}
apikey: {your_anon_key}
Authorization: Bearer {your_jwt_token}
--data-binary "@/local/path/to/your/file.ext"
```

Other SDKs (Dart, Swift, Kotlin, Python, C#) provide equivalent upload calls.

## Checked

Confirmed against the page source: 6MB guidance and 5GB ceiling, JavaScript and cURL upload forms, 400 Asset Already Exists, upsert option and x-upsert header, CDN staleness advice, content type inference and override, C# inferContentType, concurrency rules. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/storage/uploads/standard-uploads (apps/docs/content on GitHub master), read in full.
