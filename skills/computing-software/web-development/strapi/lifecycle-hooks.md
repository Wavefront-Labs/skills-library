---
id: computing-software.web-development.strapi.lifecycle-hooks
name: lifecycle-hooks
category: computing-software
field: web-development
product: strapi
tags: [strapi, lifecycles, beforecreate, aftercreate, hooks, event]
level: practitioner
status: docs-checked
description: "Write Strapi content-type lifecycle hooks in lifecycles.js: available events, the event object, and the knex caveat."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/models.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Lifecycle hooks

Triggered when Strapi queries are called, from the admin panel or custom code. They are not triggered if you use the Knex library directly. Bulk actions (`createMany`, `updateMany`, `deleteMany`) lifecycles are never triggered by a Document Service method.

## Events
`beforeCreate`, `beforeCreateMany`, `afterCreate`, `afterCreateMany`, `beforeUpdate`, `beforeUpdateMany`, `afterUpdate`, `afterUpdateMany`, `beforeDelete`, `beforeDeleteMany`, `afterDelete`, `afterDeleteMany`, `beforeCount`, `afterCount`, `beforeFindOne`, `afterFindOne`, `beforeFindMany`, `afterFindMany`.

## The event object
`action`, `model`, `params` (`data`, `select`, `where`, `orderBy`, `limit`, `offset`, `populate`), `result` (only in `after*` events), `state`.

## Declarative use
Create `lifecycles.js` in `./src/api/[api-name]/content-types/[content-type-name]/`. Listeners run sequentially, sync or async.

```js
module.exports = {
  beforeCreate(event) {
    const { data, where, select, populate } = event.params;

    // let's do a 20% discount everytime
    event.params.data.price = event.params.data.price * 0.8;
  },

  afterCreate(event) {
    const { result, params } = event;

    // do something to the result;
  },
};
```

## Checked

Checked 2026-11-04 against the Strapi Models page (lifecycle hooks: knex caveat, Document Service bulk note, available events, event object, declarative usage). Nothing removed.

Method: documentation only; no commands were run.
