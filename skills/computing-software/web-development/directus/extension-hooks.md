---
id: computing-software.web-development.directus.extension-hooks
name: extension-hooks
category: computing-software
field: web-development
product: directus
tags: [extension-hooks, hook-filter, hook-action, hook-register-context]
level: advanced
status: docs-checked
description: "Write a Directus hook extension: the register function with filter, action, init, schedule and embed, the context object and blocking filter caveats."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/09.extensions/2.api-extensions/1.hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `index.js` or `index.ts` entrypoint exports a function that registers listeners:

```js
export default ({ filter, action }) => {
  filter("items.create", (payload, meta, context) => {
    console.log("About to create item.");
    return payload;
  });
  action("items.create", (meta, context) => {
    console.log("Item created!");
  });
};
```

Register types: `filter` (before the event; check, modify or prevent it), `action` (after; enrichment, automations), `init` (lifecycle points), `schedule` (time interval), `embed` (inject JS or CSS into the Studio).

Second argument (context): `services`, `database` (Knex), `getSchema`, `env`, `logger` (Pino), `emitter`.

Filter callback: modifiable `payload`, `meta` (`event`, `collection`), `context` (`database` transaction, `schema`, `accountability`). Action callback: `meta` with `event`, `payload`, `key`, `collection`, plus `context`.

Example events: `items.create`, `items.update`, `items.delete`, `<collection>.items.read`, `auth.login`, `files.upload`, `server.start`, `websocket.message`.

Gotcha: filters are blocking and can hurt performance, especially on `read` events that trigger many database reads.

## Checked

2026-11-04: confirmed against the Directus docs Event Hooks page: register types, context properties, filter and action meta and context properties, listed event names, filters-are-blocking warning. Removed the unsupported verify line.

Method: documentation only; no commands were run.
