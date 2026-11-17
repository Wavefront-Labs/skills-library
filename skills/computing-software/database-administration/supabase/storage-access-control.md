---
id: computing-software.database-administration.supabase.storage-access-control
name: storage-access-control
category: computing-software
field: database-administration
product: supabase
tags: [storage, access-control, storage-objects, foldername, policies]
level: practitioner
status: docs-checked
description: "Write Supabase Storage RLS policies on storage.objects: insert-only uploads, upsert needs, per-user folders, owner reads and allow_any_operation."
sources:
  - https://supabase.com/docs/guides/storage/security/access-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authorise Storage operations with RLS.

Storage blocks all uploads to buckets without policies, so allow each operation explicitly. Policies go on `storage.objects`. Uploads need only `INSERT`; `upsert` overwrites also need `SELECT` and `UPDATE`. Public buckets need no policy for public reads. Service keys bypass RLS entirely, so keep them private.

Helpers: `storage.foldername(name)`, `storage.allow_only_operation()`, `storage.allow_any_operation()`, `auth.jwt()`. Use the allow functions when different storage actions need different `SELECT` policies; in the avatar example `allow_any_operation()` stops users listing the bucket.

Uploads by authenticated users into a folder named after their ID:

```sql
create policy "Allow authenticated uploads"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'my_bucket_id' and
  (storage.foldername(name))[1] = (select auth.jwt()->>'sub')
);
```

Restrict to a fixed folder by comparing `(storage.foldername(name))[1] = 'private'`.

Users read their own uploads:

```sql
create policy "Individual user Access"
on storage.objects for select
to authenticated
using ( (select auth.jwt()->>'sub') = owner_id );
```

Public avatar reads for holders of the publishable key:

```sql
create policy "Avatar images are publicly accessible." on storage.objects
  for select using (bucket_id = 'avatars' and
  storage.allow_any_operation(array['object.get_authenticated_info', 'object.get_authenticated']));
```

## Checked

Confirmed against the page: no uploads without RLS policies, INSERT only for uploads, SELECT and UPDATE additionally for upsert, storage.foldername, storage.allow_only_operation and allow_any_operation, all four policy examples, service key bypass. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/storage/security/access-control (apps/docs/content on GitHub master), read in full.
