---
id: computing-software.web-development.payload-cms.root-components
name: root-components
category: computing-software
field: web-development
product: payload-cms
tags: [root-components, admin-header, before-dashboard, nav-links]
level: advanced
status: docs-checked
description: "Inject Custom Components into the Admin Panel dashboard, login, nav, header and settings menu using admin.components."
sources:
  - https://payloadcms.com/docs/custom-components/root-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Root Components

Goal: customise global Admin Panel areas.

```ts
export default buildConfig({
  admin: {
    components: {
      beforeDashboard: ['/components/BeforeDashboard#BeforeDashboard'],
      afterNavLinks: ['/components/NavFooter#NavFooter'],
      graphics: { Logo: '/components/Logo#Logo', Icon: '/components/Icon#Icon' },
    },
  },
})
```

Options in the docs table: `actions` (header, extra interactivity), `afterDashboard`, `beforeDashboard`, `afterLogin`, `beforeLogin`, `afterNavLinks`, `beforeNavLinks`, `graphics.Icon` (simplified logo used in the Nav), `graphics.Logo` (full logo on the Login view), `header` (above the Payload header), `logout.Button`, `Nav` (the whole sidebar and mobile menu), `settingsMenu` (gear icon popup above logout), `providers` (React Context providers wrapping the Admin), `views`.

Verify: your logo appears on the login screen.

## Checked

2026-11-04. Read custom-components/root-components. Confirmed: the admin.components option table (actions, afterDashboard, beforeDashboard, afterLogin, beforeLogin, afterNavLinks, beforeNavLinks, graphics.Icon as the simplified logo, graphics.Logo as the full logo on Login, header above the Payload header, logout.Button, Nav as the whole sidebar and mobile menu, settingsMenu behind the gear icon, providers, views). Removed: the unconfirmed sentence about array and singular options replacing defaults.
Method: documentation only; no commands were run.
