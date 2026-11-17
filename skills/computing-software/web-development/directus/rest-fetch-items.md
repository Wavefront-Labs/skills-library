---
id: computing-software.web-development.directus.rest-fetch-items
name: rest-fetch-items
category: computing-software
field: web-development
product: directus
tags: [rest-fetch-items, items-endpoint, static-token, default-limit]
level: intro
status: docs-checked
description: "Read items from a Directus collection over REST with a static admin token, using filter and fields query parameters and the 100-item default limit."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/getting-started/4.use-the-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisite: a collection (example `posts`) and a static token. In the Data Studio open your user detail page, create a token, note it, then save.

```bash
curl \
  --header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  --url 'https://directus.example.com/items/posts'
```

Replace the base URL with your project URL and `posts` with your collection name.

Add global query parameters to shape the result:

```bash
curl --header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  --url 'https://directus.example.com/items/posts?filter[status][_eq]=published&fields=id,title'
```

That returns only `published` items and only `id` and `title`.

The default limit is 100. With more items, provide a higher `limit` or request a second page.

## Checked

2026-11-04: confirmed against the Directus docs Use the API page (Fetching Data, Using Query Parameters): admin static token steps, curl examples, filter and fields example, default limit of 100. Removed the unsupported verify line.

Method: documentation only; no commands were run.
