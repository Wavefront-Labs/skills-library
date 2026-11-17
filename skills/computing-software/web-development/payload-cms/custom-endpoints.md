---
id: computing-software.web-development.payload-cms.custom-endpoints
name: custom-endpoints
category: computing-software
field: web-development
product: payload-cms
tags: [custom-endpoints, endpoint-handler, routeparams, root-endpoint]
level: advanced
status: docs-checked
description: "Add custom REST endpoints to a collection, global or root config using path, method and handler."
sources:
  - https://payloadcms.com/docs/rest-api/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom endpoints

Goal: add your own routes to the Payload API.

Endpoint options: `path` (route after the collection or global slug), `method` (lowercase: `get`, `head`, `post`, `put`, `delete`, `connect` or `options`), `handler` (receives the `PayloadRequest`, a Web Request with `req.payload`, `req.user`), `root` (top-level endpoints only: mount at the root, bypassing `routes.api`) and `custom`.

```ts
export const Orders: CollectionConfig = {
  slug: 'orders',
  fields: [],
  endpoints: [
    {
      path: '/:id/tracking',
      method: 'get',
      handler: async (req) => {
        const tracking = await getTrackingInfo(req.routeParams.id)
        if (!tracking) return Response.json({ error: 'not found' }, { status: 404 })
        return Response.json(tracking)
      },
    },
  ],
}
```

This route is served at `/api/orders/:id/tracking`. Set `endpoints: false` to disable a collection's routes. Root-level endpoints go in the root config's `endpoints` array.

Warning: custom endpoints are not authenticated by default, so check `req.user` yourself. Helpers: `req.json()` for the body, `addDataAndFileToRequest` for parsing data and files, and `headersWithCors` for CORS headers. The docs' handlers return a Web `Response`. Call access-controlled Local API operations with `req.user` and `overrideAccess: false`.

## Checked

2026-11-04. Read rest-api/overview (custom endpoints) and configuration/collections (endpoints option) in the payloadcms/payload docs. Confirmed: path, method, handler, root, custom, endpoints: false. Added: not-authenticated warning, method list, helpers. Softened: Response requirement is shown in examples only. Removed: the verify step.
Method: documentation only; no commands were run.
