---
id: computing-software.web-development.strapi.list-and-generate-commands
name: list-and-generate-commands
category: computing-software
field: web-development
product: strapi
tags: [strapi, routes-list, policies-list, middlewares-list, strapi-generate, cli]
level: intro
status: docs-checked
description: "Strapi CLI listing commands (routes:list, policies:list, middlewares:list...) to check names, and strapi generate to scaffold."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/cli.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/routes.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/policies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Listing and generating

## Listing
The CLI page groups these listing commands:

`routes:list`, `policies:list`, `middlewares:list`, `content-types:list`, `components:list`, `hooks:list`, `controllers:list`, `services:list`.

```bash
yarn strapi routes:list
yarn strapi policies:list
yarn strapi middlewares:list
```

- `routes:list` displays all available routes (the routes page: existing routes and their hierarchical order).
- `policies:list` displays all registered policies.
- `middlewares:list` displays all registered middlewares.

## Generating
`strapi generate` shows an interactive menu: api, controller, content-type, policy, middleware, migration, service. It detects TypeScript or JavaScript automatically. Singular and plural names must be different and use kebab-case.

## Checked

Checked 2026-11-04 against the Strapi CLI page (listing and generate sections), the routes page and the policies page. Removed the claims that the list commands are for checking names, the middleware prompt description and the typo self-check, none of which the pages state.

Method: documentation only; no commands were run.
