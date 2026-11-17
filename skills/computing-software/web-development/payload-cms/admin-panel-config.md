---
id: computing-software.web-development.payload-cms.admin-panel-config
name: admin-panel-config
category: computing-software
field: web-development
product: payload-cms
tags: [admin-panel, admin-user, admin-routes, admin-options]
level: practitioner
status: docs-checked
description: "Configure the Admin Panel via the admin option: user collection, routes, timezones, toast, theme, autoLogin and project structure."
sources:
  - https://payloadcms.com/docs/admin/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Admin Panel configuration

Goal: configure the Admin Panel from the root `admin` option.

Options: `avatar` (`gravatar`, `default` or a component), `autoLogin`, `autoRefresh`, `components`, `constrainWidth` (experimental), `custom`, `dateFormat` (date-fns pattern), `livePreview`, `meta`, `routes`, `suppressHydrationWarning`, `theme` (restrict to one theme, default `all`), `timezones`, `toast`, `user`.

```ts
export default buildConfig({
  admin: {
    user: 'admins',   // collection allowed to log in to the Admin Panel
    timezones: {
      supportedTimezones: [{ label: 'Los Angeles', value: 'America/Los_Angeles' }],
      defaultTimezone: 'America/Los_Angeles',
    },
    toast: { duration: 6000, limit: 5, position: 'bottom-right' },
  },
})
```

Default routes under `routes`: `admin` `/admin`, `api` `/api`, `graphQL` `/graphql`, `graphQLPlayground` `/graphql-playground` (this page lists them without an `/api` prefix, while the GraphQL page says the endpoint is `/api/graphql`); admin sub-routes include `/login`, `/logout`, `/forgot`, `/reset`, `/account`, `/create-first-user`, `/unauthorized`, `/logout-inactivity`.

`autoLogin` takes `email`, `password` and `prefillOnly` (plus `username` when logging in by username) for development or demo convenience. The docs example gates it behind an environment check such as `NODE_ENV` so it is disabled in production.

Next.js layout: `app/(payload)/admin/[[...segments]]/page.tsx`, `api/[...slug]/route.ts`, `graphql/route.ts`, `graphql-playground/route.ts`, `custom.css`, `layout.tsx`. The `(payload)` folder can be moved by updating `routes` and `admin.importMap`.

Only the collection named in `admin.user` can log in to the Admin Panel; `/admin` is the default admin route.

## Checked

2026-11-04. Read admin/overview and authentication/overview (autoLogin) in the payloadcms/payload docs. Confirmed: option list, routes, toast defaults (duration 6000, limit 5, position bottom-right), project structure. Reworded: autoLogin guidance to match the docs example. Flagged: the admin page and the GraphQL page differ on whether the GraphQL path carries the /api prefix.
Method: documentation only; no commands were run.
