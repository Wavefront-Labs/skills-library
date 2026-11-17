---
id: computing-software.web-development.strapi.production-build-launch
name: production-build-launch
category: computing-software
field: web-development
product: strapi
tags: [strapi, deployment, production, build, start, environment]
level: practitioner
status: docs-checked
description: "Deploy Strapi to production: env-driven host and port, NODE_ENV=production build, and launching with strapi start."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/deployment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Production build and launch

1. Configure through environment variables, using the `env` helper in config files:

```js
module.exports = ({ env }) => ({
  host: env('HOST', '0.0.0.0'),
  port: env.int('PORT', 1337),
});
```

2. Build the admin panel for production:

```bash
NODE_ENV=production yarn build
```

3. Run the server with production settings: `NODE_ENV=production yarn start` (or `NODE_ENV=production npm run start`). The page recommends a process manager such as PM2.

- On Windows, install `cross-env` and add scripts such as `"build:win": "cross-env NODE_ENV=production npm run build"` and `"start:win": "cross-env NODE_ENV=production npm run start"`.
- A new project gets a `.env` file with default values; edit it or set variables on the hosting platform.
- A `./server.js` containing `require('@strapi/strapi').createStrapi(/* {...} */).start()` allows `node server.js`; TypeScript projects must provide the `distDir` option.
- `/_health` answers `204 No Content` when the server is ready.
- In CI, set `NODE_ENV=production` on the build step only (setting it job-wide skips devDependencies on install), inject secrets (`APP_KEYS`, `API_TOKEN_SALT`, `ADMIN_JWT_SECRET`, `JWT_SECRET`, `TRANSFER_TOKEN_SALT`, `ENCRYPTION_KEY`, database credentials) from the CI tool, and keep them the same across deployments: regenerating `APP_KEYS`, `ADMIN_JWT_SECRET` or `JWT_SECRET` invalidates existing sessions and API tokens.
- Content-types cannot be created or updated in production; schema changes come from deployed code. Removing a content-type drops its table on start.
- For self-hosted Kubernetes, the page recommends npm over pnpm.

Related: `computing-software.web-development.strapi.server-config-file`, `computing-software.web-development.strapi.environment-variables`, `computing-software.web-development.strapi.dev-start-build-commands`.

## Checked

2026-11-04: checked against the Strapi docs page Deployment (deployment). Confirmed: the env helper config, the `NODE_ENV=production` build, the production start command, `cross-env` scripts. Removed: the claim that `develop` should never be used in production because of auto-reload and the Content-type Builder, which the page does not state. Added from the page: PM2 recommendation, server.js and distDir, the health check route, CI secrets and NODE_ENV guidance, schema sync caution, npm over pnpm for Kubernetes.

Method: documentation only; no commands were run.
