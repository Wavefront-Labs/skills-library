---
id: computing-software.web-development.strapi.server-config-file
name: server-config-file
category: computing-software
field: web-development
product: strapi
tags: [strapi, config-server, host, port, app-keys, proxy, url]
level: practitioner
status: docs-checked
description: "config/server options: host, port, app.keys, public url, proxy and IP header trust, cron, dirs, openapi endpoints."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/server.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/deployment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# config/server

Changes require rebuilding the admin panel (`yarn build` or `npm run build`).

| Option | Meaning | Default |
|---|---|---|
| `host` (mandatory) | host name | `localhost` |
| `port` (mandatory) | port | `1337` |
| `app.keys` (mandatory) | Koa session keys used by the session middleware | - |
| `url` | public URL; needed for reset password, third-party login, and absolute URLs behind a proxy (Apache, Nginx) | - |
| `proxy.koa` | set Koa `app.proxy`; true trusts proxy headers | `false` |
| `proxy.ipHeader` | proxy IP header to trust (5.52.0+) | `'X-Forwarded-For'` |
| `proxy.maxIpsCount` | max IPs read from that header; set when behind a reverse proxy to prevent spoofing (5.52.0+); `0` (Koa default) means unlimited, which is insecure behind a proxy | `0` |
| `cron.enabled` | enable cron jobs | `false` |
| `dirs.public` | public folder path | `./public` |
| `webhooks.defaultHeaders` | default webhook headers | `{}` |

`emitErrors` was removed in Strapi 5. The `openapi` option has `content-api` and `admin` endpoints that are `access: 'disabled'` by default.

Example from the page:

```js
module.exports = ({ env }) => ({
  host: env('HOST', '0.0.0.0'),
  port: env.int('PORT', 1337),
});
```

## Checked

Checked 2026-11-04 against the Strapi Server configuration page (caution on rebuilding, available options table, examples). Corrected the `proxy.ipHeader` and `proxy.maxIpsCount` defaults and renamed the example heading, which the page does not call a production pattern.

Method: documentation only; no commands were run.
