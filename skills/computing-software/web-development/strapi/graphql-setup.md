---
id: computing-software.web-development.strapi.graphql-setup
name: graphql-setup
category: computing-software
field: web-development
product: strapi
tags: [strapi, graphql, plugin, endpoint, playground, upload-limitation]
level: practitioner
status: docs-checked
description: "Install the Strapi GraphQL plugin, its single /graphql endpoint, plugin config defaults, and the upload limitation."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/graphql.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GraphQL setup

Install the plugin:

```sh
yarn add @strapi/plugin-graphql
```

```sh
npm install @strapi/plugin-graphql
```

The playground is then at `/graphql`. One endpoint handles all queries and mutations, configured in the plugins config file. Defaults shown on the page:

```js
  export default {
    shadowCRUD: true,
    endpoint: '/graphql', // <= single GraphQL endpoint
    subscriptions: false,
    maxLimit: -1,
    apolloServer: {},
    v4CompatibilityMode: process.env.STRAPI_GRAPHQL_V4_COMPATIBILITY_MODE ?? false,
  };
```

(The page places this block in the plugins configuration file, `/config/plugins.js|ts`; see the GraphQL plugin page's code-based configuration for the exact nesting.)

## Limits to know
- No media upload via GraphQL: use REST `POST /upload` and link the returned file.
- Documents are exposed only by `documentId`; the numeric `id` is not available (REST still returns it).
- Each content-type gets two queries named after its singular and plural API IDs.

## Checked

Checked 2026-11-04 against the Strapi GraphQL API page (installation, playground, endpoint configuration, upload note, `documentId` caution). Nothing removed.

Method: documentation only; no commands were run.
