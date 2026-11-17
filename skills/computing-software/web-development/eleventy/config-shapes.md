---
id: computing-software.web-development.eleventy.config-shapes
name: config-shapes
category: computing-software
field: web-development
product: eleventy
tags: [config-file, callback-function, return-object, export-default, async-config]
level: intro
status: docs-checked
description: "Choose the shape of an Eleventy config file: the preferred callback function, the optional return object, or a plain default-exported options object."
sources:
  - https://www.11ty.dev/docs/config-shapes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three shapes are accepted.

**1. Callback function (preferred).** Gives access to the full Configuration API. ESM and async callbacks need Eleventy v3.0.0+.

```js
export default async function (eleventyConfig) {
  // API calls here
}
export const config = { dir: { input: "views" } };
```

Static options go in a named `config` export.

**2. Return object (not preferred, for order-of-operations reasons).** Return the same options object from the callback:

```js
export default async function (eleventyConfig) {
  return { dir: { input: "views", output: "dist" } };
}
```

**3. Default-exported object.** Static options only, no API access:

```js
export default { dir: { input: "views" } };
```

Use the callback unless you only need static options. For default file names, see the config skills.

## Checked

2026-11-04. Confirmed against the Eleventy Configuration Shapes page: callback function preferred, ESM and async callbacks added in v3.0.0, optional named config export, returned object not preferred for order-of-operations reasons, default-exported static object without API access. Corrected the version gate from 3.0.0-alpha.1 to v3.0.0.

Method: documentation only; no commands were run.
