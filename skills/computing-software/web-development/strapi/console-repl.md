---
id: computing-software.web-development.strapi.console-repl
name: console-repl
category: computing-software
field: web-development
product: strapi
tags: [strapi, console, repl, debugging, strapi-object, query-engine]
level: practitioner
status: docs-checked
description: "Use strapi console to open a Node REPL with the loaded app and call services, controllers, content-types and the DB."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# strapi console

```bash
strapi console
```

Compiles and loads the application, starts the server in the background, then opens a Node.js REPL. Use it to test code and inspect the project with direct access to the `strapi` object.

## Helpers listed on the page
- `strapi.services` and `strapi.service(uid)`
- `strapi.controllers` and `strapi.controller(uid)`
- `strapi.contentTypes` and `strapi.contentType(uid)`
- `strapi.components`
- `strapi.policies` and `strapi.policy(name)`
- `strapi.middlewares` and `strapi.middleware(name)`
- `strapi.plugins` and `strapi.plugin(name)`
- `strapi.hooks` and `strapi.hook(name)`
- `strapi.apis` and `strapi.api(name)`
- `strapi.db`, to query the database through the Query Engine API:

```js
await strapi.db.query('api::article.article').findMany();
```

Context is available anywhere thanks to Node.js AsyncLocalStorage.

## Checked

Checked 2026-11-04 against the Strapi CLI page (`strapi console` section and helper list). Nothing removed.

Method: documentation only; no commands were run.
