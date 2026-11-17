---
id: computing-software.database-administration.supabase.signed-urls-and-downloads
name: signed-urls-and-downloads
category: computing-software
field: database-administration
product: supabase
tags: [storage, signed-url, create-signed-url, download, revocation]
level: practitioner
status: docs-checked
description: "Serve private Supabase Storage files with createSignedUrl, custom download names, and revoking signed URLs by deleting objects or rotating the signing key."
sources:
  - https://supabase.com/docs/guides/storage/serving/downloads
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: hand out time-limited access to private files and be able to revoke it.

Create a signed URL; the second argument is expiry in seconds:

```js
const { data, error } = await supabase.storage
  .from('bucket')
  .createSignedUrl('private-document.pdf', 3600)
if (data) console.log(data.signedUrl)
```

Assets in a non-public bucket are unreachable by public URL. Access is only via a signed URL or an authenticated GET with the user's Authorization header at `/storage/v1/object/authenticated/[bucket]/[asset-name]`.

Download with a custom name:

```js
const { data, error } = await supabase.storage.from('avatars').download('avatar1.png', {
  download: 'my-custom-name.png',
})
```

On a URL, `?download` forces a download and `?download=customname.jpg` names it. Dart uses `queryParams` and Swift `queryItems` for the same parameter.

Revocation:
- Individual signed URLs cannot be revoked. Deleting, moving or renaming the underlying object invalidates them.
- Storage signs URLs with its own key, so Auth JWT key changes do not affect them.
- Rotating the key on the URL Signing Keys dashboard page revokes all signed URLs; old ones return `InvalidJWT`.
- Exactly one key is active and one standby; URLs signed by either are accepted, and revoking a key rejects URLs signed with it.
- URLs already served may still come from CDN cache; purge it.

## Checked

Confirmed against the downloads page: createSignedUrl with expiry in seconds, authenticated URL form, download option and ?download parameter, Dart queryParams and Swift queryItems, no per-URL revocation (delete, move or rename the object). Confirmed against the URL signing keys page: dedicated Storage key separate from Auth keys, rotate then revoke, InvalidJWT after revoking, one active and one standby key, CDN cache can still serve cached signed URLs until purged. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/storage/serving/downloads and guides/storage/security/signing-keys (apps/docs/content on GitHub master), read in full.
