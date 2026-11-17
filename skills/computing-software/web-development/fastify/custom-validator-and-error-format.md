---
id: computing-software.web-development.fastify.custom-validator-and-error-format
name: custom-validator-and-error-format
category: computing-software
field: web-development
product: fastify
tags: [fastify, validation, validator-compiler, errors, schema-error-formatter]
level: advanced
status: docs-checked
description: "Replace the validator with setValidatorCompiler and shape validation errors with schemaErrorFormatter or attachValidation."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Validation-and-Serialization.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Swap in a different validator per instance or route:

```js
fastify.setValidatorCompiler(({ schema, method, url, httpPart }) => {
  return (data) => {
    const result = myValidate(schema, data)
    return result.ok ? { value: result.value } : { error: new Error('bad data') }
  }
})
```

A synchronous validator function must return `{ value }` on success or `{ error }` on failure and should not throw (wrap in try/catch and return `{ error: e }`); throwing from custom validators combined with async `preValidation` hooks causes unhandled promise rejections that can crash the app. The `{ value, error }` convention applies only to synchronous compilers: an asynchronous validator is pass/fail only and signals failure by rejecting. For the `headers` part, `value` is applied through the additive `request.headers` setter, so a validator cannot remove a header by omitting it. (`setSchemaCompiler` and `setSchemaResolver` were replaced by `setValidatorCompiler` in v3.)

Failed validation gets `statusCode` 400 by default. Fastify adds `validation` (the `error` content returned by the validator) and `validationContext` (body, params, query or headers) to the error, so a custom error handler can branch on `error.validation`. Error messages come from `schemaErrorFormatter`, which is written with Ajv in mind; other libraries may give odd messages unless they return Ajv-shaped errors.

Customize the message:

```js
fastify.setSchemaErrorFormatter((errors, dataVar) => {
  return new Error(`${dataVar}: ${errors[0].message}`)
})
```

Handle errors yourself in the handler with the route option `attachValidation: true`: no automatic 400, and `request.validationError` holds the same Error Fastify would have sent (`message` from the formatter, `validation`, `validationContext`, `code` `FST_ERR_VALIDATION`, `statusCode` 400).

```js
fastify.post('/', { schema, attachValidation: true }, (request) => {
  if (request.validationError) return { bad: request.validationError.message }
})
```

`ajv-errors` is supplied through the `ajv.plugins` option (with `errorMessage` in the schema); Fastify v5 needs an `ajv-errors` version compatible with Ajv v8. For localized messages use `ajv-i18n` inside a `setErrorHandler`. Validation error details appear in the response by default; use `setErrorHandler` to sanitize them.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Validation-and-Serialization.md, Migration-Guide-V3.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
