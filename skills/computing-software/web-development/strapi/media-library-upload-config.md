---
id: computing-software.web-development.strapi.media-library-upload-config
name: media-library-upload-config
category: computing-software
field: web-development
product: strapi
tags: [strapi, media-library, upload, sizelimit, breakpoints, sharp, providers]
level: practitioner
status: docs-checked
description: "Configure Strapi's upload package in config/plugins: sizeLimit, breakpoints, sharp, security, concurrency, and providers."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/media-library.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Media Library (upload) configuration

Declare an `upload.config` object in `config/plugins` (default provider). All parameters optional:

| Param | Meaning | Default |
|---|---|---|
| `providerOptions.localServer` | options passed to koa-static | - |
| `sizeLimit` | max file size in bytes | `1000000000` (1 GB) |
| `breakpoints` | responsive image sizes | `{ large: 1000, medium: 750, small: 500 }` |
| `sharp` | sharp image processing options | `{ cache: false, concurrency: 1 }` |
| `security` | validation rules (allowedTypes, deniedTypes) | - |
| `concurrentUploadRequests` | files the admin uploads in parallel (integer >= 1) | `1` |
| `concurrentUploadSize` | files the server processes in parallel per request (integer >= 1) | `1` |

Projects scaffolded by `create-strapi-app` set `upload.config.security.allowedTypes` and `deniedTypes`.

## Providers and private storage
Other providers (third-party storage) are installed and configured separately; their options are in the provider's docs. With a private provider (e.g. an S3 bucket with `ACL: 'private'`) file URLs are signed and expire after `signedUrlExpires`; richtext and blocks fields store the unsigned URL and are re-signed on read.

## Legacy UI
From v5.54.0 the new Media Library is the default; restore the old one with `useLegacyMediaLibrary: env.bool('USE_LEGACY_MEDIA_LIBRARY', false)` in `/config/features`.

## Checked

Checked 2026-11-04 against the Strapi Media Library page (configuration table, private providers, legacy UI, concurrent uploads, security). Removed the line on `/api/upload` and GraphQL, which the page does not state.

Method: documentation only; no commands were run.
