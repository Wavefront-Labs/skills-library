---
id: computing-software.web-development.directus.realtime-sdk-connect
name: realtime-sdk-connect
category: computing-software
field: web-development
product: directus
tags: [realtime-connect, websockets-enabled, sdk-realtime, ws-lifecycle-events]
level: practitioner
status: docs-checked
description: "Enable Directus Realtime with WEBSOCKETS_ENABLED and connect from the SDK realtime composable using a static token, with open/message/close/error hooks."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/getting-started/8.connect-to-realtime.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Realtime is disabled by default on self-hosted projects: set `WEBSOCKETS_ENABLED=true`. Directus Cloud needs no setup.

Connections and subscriptions use the permissions of the authenticated user, or public permissions if unauthenticated. Give the user a policy and a static token first.

```js
import { createDirectus, staticToken, realtime } from '@directus/sdk';

const directus = createDirectus('https://example.directus.app')
  .with(staticToken('your_access_token'))
  .with(realtime());

await directus.connect();
```

Listen to socket lifecycle events:

```js
directus.onWebSocket('open', () => console.log('open'));
directus.onWebSocket('message', (m) => console.log(m.type, m.data));
directus.onWebSocket('close', () => console.log('closed'));
directus.onWebSocket('error', (e) => console.log(e));
```

## Checked

2026-11-04: confirmed against the Directus docs Connect to Realtime Data page: WEBSOCKETS_ENABLED default off on self-hosted, permissions of the authenticated user, realtime composable with staticToken, onWebSocket events. The page imports the SDK from a CDN URL; the package import shown is the same module. Removed the unsupported troubleshooting gotcha and verify line.

Method: documentation only; no commands were run.
