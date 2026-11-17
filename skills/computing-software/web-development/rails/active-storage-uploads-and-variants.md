---
id: computing-software.web-development.rails.active-storage-uploads-and-variants
name: active-storage-uploads-and-variants
category: computing-software
field: web-development
product: rails
tags: [rails, active-storage, file-uploads, image-variants, direct-uploads, s3, vips, ruby, web-development]
level: practitioner
status: docs-checked
description: "Handling uploads with Rails Active Storage: service config, has_one_attached, variants with vips, direct uploads to S3, validations, proxy vs redirect URLs and N+1."
sources:
  - https://guides.rubyonrails.org/active_storage_overview.html
  - https://guides.rubyonrails.org/configuring.html#configuring-active-storage
  - https://github.com/rails/rails/blob/v8.1.4/activestorage/app/models/active_storage/blob.rb
  - https://github.com/rails/rails/blob/v8.1.4/activestorage/lib/active_storage/attached/model.rb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active Storage uploads and variants

**Goal:** uploads stored in object storage, images resized efficiently, files validated, and URLs served without leaking or N+1.

## 1. Setup
```bash
bin/rails active_storage:install && bin/rails db:migrate
```
```yaml
# config/storage.yml
local:  { service: Disk, root: <%= Rails.root.join("storage") %> }
amazon:
  service: S3
  access_key_id: <%= Rails.application.credentials.dig(:aws, :access_key_id) %>
  secret_access_key: <%= Rails.application.credentials.dig(:aws, :secret_access_key) %>
  region: eu-west-1
  bucket: acme-prod-uploads
```
`config.active_storage.service = :amazon` in production.

## 2. Attach
```ruby
class User < ApplicationRecord
  has_one_attached :avatar do |a|
    a.variant :thumb, resize_to_limit: [128, 128], preprocessed: true
  end
  has_many_attached :documents
end
```
Form: `form.file_field :avatar, accept: "image/png,image/jpeg", direct_upload: true`; permit `:avatar` / `documents: []` in strong parameters.

## 3. Variants
Variants use libvips by default (`config.active_storage.variant_processor` is `:vips` from `load_defaults 7.0`; `:mini_magick` and `:disabled` are the alternatives; the guide asks for libvips v8.6+ or ImageMagick installed on the host, so install it in your image). `user.avatar.variant(:thumb)` is generated on first request, or ahead of time with `preprocessed: true`. A variant tracker stores processed variants in the database; to avoid N+1 queries when rendering many representations use `with_all_variant_records`.

## 4. Validation
```ruby
validate :avatar_type_and_size
def avatar_type_and_size
  return unless avatar.attached?
  errors.add(:avatar, "must be PNG or JPEG") unless avatar.blob.content_type.in?(%w[image/png image/jpeg])
  errors.add(:avatar, "is too big") if avatar.blob.byte_size > 5.megabytes
end
```
Active Storage identifies the content type from the file contents (via Marcel) unless you pass `identify: false` with a `content_type`, so check `blob.content_type` rather than the file name. With direct uploads the blob exists before the record is saved, so clean up unattached blobs periodically (`ActiveStorage::Blob.unattached.where(created_at: ..2.days.ago).find_each(&:purge_later)`).

## 5. Direct uploads
Include the `@rails/activestorage` JS and call `ActiveStorage.start()`. Configure CORS on the storage service to allow all origins your app is served from, the `PUT` method and the `Content-Type`, `Content-MD5` and `Content-Disposition` headers (plus `Cache-Control` for GCS if `cache_control` is set); the Disk service needs no CORS. Files go browser to storage, sparing your app servers.

## 6. Serving
- `url_for(user.avatar)` -> redirect mode: a stable signed route that redirects to the service endpoint, with an HTTP expiration of 5 minutes. Links are shareable until expiry.
- Proxy mode (`rails_storage_proxy_path` or `config.active_storage.resolve_model_to_route = :rails_storage_proxy`) streams through the app - put a CDN in front.
- Private files: authorise in your own controller and redirect to `blob.url(expires_in: 1.minute)`.
- For some content types (HTML, SVG and similar) Active Storage forces `Content-Disposition: attachment` to prevent XSS; the list is `config.active_storage.content_types_to_serve_as_binary` - keep it that way.

## 7. Performance
`User.with_attached_avatar` preloads attachments and blobs (avoids N+1). `purge_later` on removal.

## Verify
- [ ] Listing 50 users with avatars runs a constant number of queries.
- [ ] Uploading a renamed `.exe` as `.jpg` is rejected.
- [ ] Variant generation works in production (libvips installed) and URLs expire.

## Checked
Checked 2026-10-24 against the Rails 8.1.4 Active Storage and configuring guides and the v8.1.4 blob and attached-model sources. Confirmed: `active_storage:install`, named variants with `preprocessed: true`, vips default from 7.0 and the `variant_processor` values, `with_all_variant_records` for N+1, direct upload CORS requirements, 5-minute redirect expiry, `rails_storage_proxy` route resolution, `content_types_to_serve_as_binary`, `purge_later`, the `unattached` scope, Marcel type detection and `with_attached_<name>`. Removed the `active_storage_validations` gem mention and the WebP/AVIF conversion advice, which the checked pages do not cover.

Method: documentation only; no commands were run.
