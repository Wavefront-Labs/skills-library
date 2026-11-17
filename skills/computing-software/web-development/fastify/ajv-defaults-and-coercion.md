---
id: computing-software.web-development.fastify.ajv-defaults-and-coercion
name: ajv-defaults-and-coercion
category: computing-software
field: web-development
product: fastify
tags: [fastify, validation, ajv, coercion, defaults]
level: advanced
status: docs-checked
description: "Know the default Ajv options Fastify sets and how coercion, defaults and union types behave."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Validation-and-Serialization.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V4.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Recommendations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default Ajv options: `coerceTypes: 'array'`, `useDefaults: true`, `removeAdditional: true`, `uriResolver: require('fast-uri')`, `addUsedSchema: false`, `allErrors: false`.

Tune them with the factory `ajv` option (`customOptions`, `plugins`, `onCreate`):

```js
const fastify = require('fastify')({
  ajv: {
    customOptions: { removeAdditional: 'all' },
    plugins: [require('ajv-merge-patch')],
    onCreate: (ajv) => {
      ajv.addFormat('myFormat', (data) => typeof data === 'string')
    }
  }
})
```

Alternatively pass your own instance with `fastify.setValidatorCompiler(({ schema, method, url, httpPart }) => ajv.compile(schema))`; then add schemas to that validator, because Fastify's `addSchema` will not recognize it. Ajv plugins must be compatible with the Ajv version shipped in Fastify.

Behavior:
- Ajv coerces values to the types in the schema `type` keywords, both to pass validation and for later use; the default supports coercing array parameters in `querystring` (`?ids=1` gives `["1"]` for an `array` type).
- `removeAdditional: true` strips extra properties only where `additionalProperties: false`.
- `useDefaults` fills missing properties and items from `default`.
- With coercion enabled, `anyOf` with a `{ type: 'null' }` branch first can coerce `0` or `false` to null; use `{ type: 'number', nullable: true }` instead.
- Ajv v8 (Fastify v4+) prohibits `type` keywords with multiple types other than `null` (strictTypes warning); use `anyOf` instead of `type: ['object','array']`.
- v5: `time` and `date-time` formats enforce a timezone; `iso-time` / `iso-date-time` accept an optional timezone.

Keep `allErrors` false: setting it to true makes a DoS attack possible.

Gotcha: `$async` Ajv schemas should not be used for the initial validation (database access during validation can enable DoS).

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Validation-and-Serialization.md, Migration-Guide-V4.md, Recommendations.md) and confirmed. Removed or corrected: the uriResolver default is now written as require('fast-uri') as the page shows; the invented Verify step.

Method: documentation only; no commands were run.
