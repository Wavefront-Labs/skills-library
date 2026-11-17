---
id: computing-software.web-development.directus.realtime-subscribe-and-send
name: realtime-subscribe-and-send
category: computing-software
field: web-development
product: directus
tags: [realtime-subscribe, subscribe-event, send-message, realtime-create-item]
level: practitioner
status: docs-checked
description: "Subscribe to create events on a Directus collection over an SDK realtime connection and create items by sending a message on the open socket."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/getting-started/8.connect-to-realtime.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
After `await directus.connect()` (see the realtime connect skill), subscribe:

```js
const { subscription } = await directus.subscribe('messages', {
  event: 'create',
  query: { fields: ['user', 'text'] },
});

for await (const item of subscription) {
  console.log(item);
}
```

You then receive messages whenever items in the collection are created, updated or deleted (filtered here to `create`).

Create an item over the same connection:

```js
directus.sendMessage({
  type: 'items',
  collection: 'messages',
  action: 'create',
  data: { text: 'Hello World!', user: 'Ben' },
});
```

Requirements: the user's policy needs `read` and `create` on the collection; the example collection had a `date_created` field enabled.

## Checked

2026-11-04: confirmed against the Directus docs Connect to Realtime Data page (Subscribe to Changes, Create an Item): subscribe options, sendMessage payload, policy needing read and create. Removed the unsupported verify line.

Method: documentation only; no commands were run.
