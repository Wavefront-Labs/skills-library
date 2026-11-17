---
id: computing-software.web-development.strapi.custom-field-registration
name: custom-field-registration
category: computing-software
field: web-development
product: strapi
tags: [strapi, custom-fields, customfields-register, plugin, server-register, admin]
level: advanced
status: docs-checked
description: "Register a Strapi custom field on the server with strapi.customFields.register, and the limits of what custom fields can be."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/custom-fields.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom fields

Add new field types to content-types and components. Recommended route is a plugin; app-specific ones can be registered in the global `register` function of `src/index`.

## Limits
- Distribution on the Marketplace only through plugins.
- They must use existing built-in data types and cannot modify one.
- Relation, media, component and dynamic zone types cannot be used.
- A custom field plugin has a server part and an admin part; both must register it.

## Server registration
`strapi.customFields.register()` takes an object or an array of objects:

```js
module.exports = ({ strapi }) => {
strapi.customFields.register({
  name: "color",
  plugin: "color-picker",
  type: "string",
  inputSize: {
    // optional
    default: 4,
    isResizable: true,
  },
});
};
```

File: `/src/plugins/color-picker/server/register.js`. Without a scaffolded plugin, declare it in `strapi-server.js` inside `register({ strapi })`. If `inputSize` is given it must contain all of its parameters.

## Admin registration
Also register with `app.customFields.register()` during the plugin's admin register lifecycle, so it appears in the Content-type Builder and Content Manager. In schemas, the attribute type is `customField`.

## Checked

Checked 2026-11-04 against the Strapi Custom fields page (limits, server registration, admin registration). Nothing removed.

Method: documentation only; no commands were run.
