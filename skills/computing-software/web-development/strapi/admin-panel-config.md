---
id: computing-software.web-development.strapi.admin-panel-config
name: admin-panel-config
category: computing-software
field: web-development
product: strapi
tags: [strapi, config-admin, admin-url, serveadminpanel, tutorials, notifications]
level: intro
status: docs-checked
description: "config/admin basics: autoOpen, serveAdminPanel, admin url, host and port, and disabling tutorials and release notifications."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/admin-panel.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# config/admin

## Behavior
| Param | Meaning | Default |
|---|---|---|
| `autoOpen` | open the admin on start | `true` |
| `watchIgnoreFiles` | extra files not watched in development (chokidar `ignored` filtering) | `[]` |
| `serveAdminPanel` | if false, the panel isn't served and `auth.secret` isn't required at startup (index.html is still served) | `true` |

## Server
By default the panel is at `http://localhost:1337/admin`.

| Param | Meaning | Default |
|---|---|---|
| `url` | path to the panel; relative URLs are joined to the server URL (`/dashboard` gives `http://localhost:1337/dashboard`) | `/admin` |
| `host` | host for the admin server | `localhost` |
| `port` | port for the admin server (typed string in the table) | `8000` |

If the admin panel and back end are not on the same server, set the admin `host` and `port` too. With the host and port left untouched in the server config, updating `config/admin` alone is enough to change the path.

Adding a path to `url` does not prefix your application; use a proxy such as Nginx for that.

## UI toggles (in `src/admin/app`)
```js
const config = {
  // ... other customization options go here
  tutorials: false,
  notifications: { releases: false },
};
export default {
  config,
};
```

`tutorials: false` hides the tutorial videos box; `notifications.releases: false` disables new-release notifications. These two keys belong in `src/admin/app`, not `config/admin`.

## Checked
Confirmed 2026-11-08 against the Strapi admin panel configuration page: the behavior and server sections and the app-file note (about the first 100 lines, read in full). The rest of the long page (session management, auth, features, full examples) was not read and is out of scope. Corrected the `url` default to `/admin` and `watchIgnoreFiles` default to `[]`; added the host and port guidance.
Method: docs-only read of cited pages, 2026-11-08
