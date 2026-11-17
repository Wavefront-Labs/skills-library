---
id: computing-software.web-development.directus.rest-create-item
name: rest-create-item
category: computing-software
field: web-development
product: directus
tags: [rest-create-item, post-items, json-payload]
level: intro
status: docs-checked
description: "Create a new item in any Directus collection by sending a JSON POST to /items/<collection> with a bearer token."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/getting-started/4.use-the-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All collections have consistent endpoints. POST an object of the collection's properties to `/items/<collection>` to create an item:

```bash
curl \
  --request POST \
  --header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{ "title": "Hello Universe!" }' \
  --url 'https://directus.example.com/items/posts'
```

Replace the base URL and collection name with yours. The full parameter list for each endpoint is in the API Reference, which shows REST, GraphQL and SDK examples.

## Checked

2026-11-04: confirmed against the Directus docs Use the API page (Creating Data): consistent endpoints, POST to /items/posts, curl example, API Reference note. Removed the permission step, the missing Content-Type failure gotcha and the verify line, which the page does not state.

Method: documentation only; no commands were run.
