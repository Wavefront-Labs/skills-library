---
id: computing-software.web-development.payload-cms.live-preview-frontend
name: live-preview-frontend
category: computing-software
field: web-development
product: payload-cms
tags: [live-preview-client, uselivepreview, refreshrouteonsave, server-live-preview]
level: advanced
status: docs-checked
description: "Connect a frontend to Live Preview with useLivePreview (client) or RefreshRouteOnSave (server components), depth and CSP considerations."
sources:
  - https://payloadcms.com/docs/live-preview/client
  - https://payloadcms.com/docs/live-preview/server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Live Preview in the frontend

Goal: make your site react to editor changes.

Client-side (React): `npm install @payloadcms/live-preview-react` (a Vue package also exists).

```tsx
'use client'
import { useLivePreview } from '@payloadcms/live-preview-react'

export const PageClient = ({ page: initialPage }) => {
  const { data } = useLivePreview({
    initialData: initialPage,
    serverURL: PAYLOAD_SERVER_URL,
    depth: 2,
  })
  return <h1>{data.title}</h1>
}
```

Hook arguments: `serverURL` (required), `initialData`, `depth` (default `0`), `apiRoute` (default `/api`). It returns `data` and `isLoading`.

Server-rendered pages: install the same package, fetch with `draft: true`, and render `RefreshRouteOnSave`, a client component that calls `router.refresh()` when the editor saves:

```tsx
const page = await payload.findByID({ collection: 'pages', overrideAccess: false, user, id, draft: true })
return (<><RefreshRouteOnSave /><h1>{page.title}</h1></>)
```

Add `trash: true` to the query if you want to preview trashed documents.

Gotcha: if the iframe refuses to connect, adjust your Content-Security-Policy `frame-ancestors` to allow the admin origin.

Verify: typing in the editor updates the preview without saving.

## Checked

2026-11-04. Read live-preview/client and live-preview/server. Confirmed: the @payloadcms/live-preview-react and Vue packages, useLivePreview arguments (serverURL required, initialData, depth default 0, apiRoute default /api), the data and isLoading return values, RefreshRouteOnSave calling router.refresh() with draft: true, trash: true for trashed documents, and the frame-ancestors CSP fix. Added the live-preview/server page to sources because RefreshRouteOnSave is documented there.
Method: documentation only; no commands were run.
