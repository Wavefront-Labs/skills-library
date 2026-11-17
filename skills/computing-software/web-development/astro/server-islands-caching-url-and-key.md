---
id: computing-software.web-development.astro.server-islands-caching-url-and-key
name: server-islands-caching-url-and-key
category: computing-software
field: web-development
product: astro
tags: [server-islands-caching, referer-header, astro-key, create-key]
level: sme
status: docs-checked
description: "Cache server islands (GET vs POST over 2048 bytes), read the page URL via Referer, and pin the props encryption key with ASTRO_KEY for rolling deployments or CDNs."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/server-islands.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Caching: island data is fetched with a `GET` request, with props as an encrypted string in the URL query, so standard `Cache-Control` headers work. Browsers limit URLs to 2048 bytes; beyond that Astro sends a `POST` with props in the body, which browsers do not cache and which breaks existing caching logic. Pass only necessary props.

Page URL: islands run in an isolated context, so `Astro.url` and `Astro.request.url` return something like `/_server-islands/Avatar`. Read the `Referer` header for the page address:

```astro
---
const referer = Astro.request.headers.get("Referer");

if (!referer) {
  throw new Error("Referer header is missing");
}

const url = new URL(referer);
const productId = url.searchParams.get("product");
---
```

Encryption key: props are encrypted with a random key generated on each build and embedded in the server bundle. With rolling deployments (e.g. Kubernetes), multi-region hosting, or a CDN caching pages with islands, frontend and backend may have different keys and props cannot be decrypted. Generate a reusable key:

```shell
astro create-key
```

Set it as the `ASTRO_KEY` environment variable (e.g. in a `.env` file) and in your CI/CD or host's build settings so the same key is reused in the bundle.

## Checked

2026-11-04. Confirmed against the Astro server islands guide: GET with encrypted query, 2048-byte limit and POST fallback, Cache-Control, isolated URL and Referer workaround, per-build random key, astro create-key and ASTRO_KEY. Nothing removed.

Method: documentation only; no commands were run.
