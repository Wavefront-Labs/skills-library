---
id: computing-software.web-development.ghost.ghost-admin-api-upload-image
name: ghost-admin-api-upload-image
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, image-upload, multipart, profile-image, icon]
level: practitioner
status: docs-checked
description: "Upload images to Ghost with the Admin API using multipart form data, the purpose field and a ref for path remapping."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/images/uploading-an-image.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: upload an image and use the URL Ghost returns.

Send a multipart form POST to `/ghost/api/admin/images/upload/` with fields:
- `file`: the image blob (required).
- `purpose`: default `image`; may be `profile_image` or `icon`. Supported formats for all three are WEBP, JPEG, GIF, PNG and SVG. A `profile_image` must be square. An `icon` must also be square and additionally accepts ICO.
- `ref` (optional): any identifier, such as the original file path; Ghost returns it unchanged so you can match uploads back to local references.

```bash
curl -X POST -F 'file=@/path/to/images/my-image.jpg' -F 'ref=path/to/images/my-image.jpg' \
  -H "Authorization: Ghost $token" -H "Accept-Version: $version" \
  https://{admin_domain}/ghost/api/admin/images/upload/
```

The JavaScript client call is `api.images.upload({file: '/path/to/local/file'})`.

Bulk migrations: upload each image first, then substitute the returned URL for the `ref` path in the post HTML before creating the post.

If large uploads fail behind a proxy, see the nginx upload size skill in this product.

Verify: the response includes the stored image URL and echoes your `ref`.

## Checked

2026-11-04. Confirmed: multipart fields, purpose values and default, supported formats, square rules, ICO for icon, ref echo, the upload URL and curl shape (uploading an image page); JavaScript call (Admin API JavaScript client page). Removed: nothing.

Method: documentation only; no commands were run.
