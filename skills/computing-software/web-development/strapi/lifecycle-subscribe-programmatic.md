---
id: computing-software.web-development.strapi.lifecycle-subscribe-programmatic
name: lifecycle-subscribe-programmatic
category: computing-software
field: web-development
product: strapi
tags: [strapi, lifecycles, subscribe, bootstrap, db-lifecycles, subscriber]
level: advanced
status: docs-checked
description: "Register a Strapi database lifecycle subscriber in bootstrap with strapi.db.lifecycles.subscribe, for one or all models."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/models.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Programmatic lifecycle subscribers

Instead of a per-content-type file, register a subscriber from the database layer, e.g. in `./src/index.js`:

```js
module.exports = {
  async bootstrap({ strapi }) {
// registering a subscriber
    strapi.db.lifecycles.subscribe({
      models: [], // optional;

      beforeCreate(event) {
        const { data, where, select, populate } = event.params;

        event.state = 'doStuffAfterWards';
      },

      afterCreate(event) {
        if (event.state === 'doStuffAfterWards') {
        }

        const { result, params } = event;

        // do something to the result
      },
    });
  }
}
```

- `models` is an array of content-type uids to listen to; if omitted, all content-types are listened to.
- `event.state` can share data between `beforeXXX` and `afterXXX` of one query (the page itself carries a TODO noting `state` was not yet confirmed as implemented; test it).
- A generic form `strapi.db.lifecycles.subscribe((event) => { ... })` receives every event; branch on `event.action`.

## Checked

Checked 2026-11-04 against the Strapi Models page (lifecycle hooks, programmatic usage with `strapi.db.lifecycles.subscribe`, event object table and its TODO note on `state`). Nothing removed.

Method: documentation only; no commands were run.
