---
id: computing-software.web-development.elysia.validate-with-standard-schema-and-file-uploads
name: validate-with-standard-schema-and-file-uploads
category: computing-software
field: web-development
product: elysia
tags: [elysia, validation, standard-schema, zod, valibot, file-upload, filetype]
level: advanced
status: docs-checked
description: "Use Zod, Valibot or other Standard Schema libraries in Elysia routes, mix them with t, and validate uploaded files safely with t.File or the fileType helper."
sources:
  - https://elysiajs.com/essential/validation.html
  - https://elysiajs.com/at-glance.html
  - https://elysiajs.com/tutorial/patterns/standalone-schema/
  - https://elysiajs.com/essential/life-cycle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: validate with your preferred library and keep uploads secure.

## Standard Schema

Elysia accepts any Standard Schema library: Zod, Valibot, ArkType, Effect Schema, Yup, Joi and more. Import the schema and pass it as the route option; types are inferred.

```typescript
import { Elysia } from 'elysia'
import { z } from 'zod'
import * as v from 'valibot'

new Elysia().get('/id/:id', ({ params: { id }, query: { name } }) => id, {
	params: z.object({ id: z.coerce.number() }),
	query: v.object({ name: v.literal('Lilith') })
})
```

Different libraries can be used together in the same handler. A guard with `schema: 'standalone'` and a zod body can combine with a route-level `t.Object` body.

## File uploads with t

```typescript
.post('/body', ({ body }) => body, {
	body: t.Object({
		file: t.File({ format: 'image/*' }),
		multipleFiles: t.Files()
	})
})
```

A file type makes Elysia assume `multipart/form-data` (the body parser is chosen when the object is one level deep with `t.File`).

## Files with Standard Schema

Elysia cannot check content type automatically for non-`t` schemas. Use the exported `fileType` helper, which validates by magic number:

```typescript
import { Elysia, fileType } from 'elysia'
import { z } from 'zod'

.post('/body', ({ body }) => body, {
	body: z.object({
		file: z.file().refine((file) => fileType(file, 'image/jpeg'))
	})
})
```

The docs stress using `fileType`: most validators do not really verify the file (for example checking only the declared content type), which can be a security hole.

## Gotchas

- Do not rely on a declared content type for security; use `fileType` or `t.File` with `format`.
- Coercion helpers differ by library (`z.coerce.number()` in the example, because path params arrive as strings).
- Elysia's onError code list includes `INVALID_FILE_TYPE`.

## Checked

2026-11-07. Read in full: essential/validation (Standard Schema, File, File (Standard Schema), Guard Schema Type), tutorial/patterns/standalone-schema, the validation parts of at-glance, and the Error Code list in essential/life-cycle (added as a source for the `INVALID_FILE_TYPE` gotcha). Confirmed the supported libraries, the zod and valibot example, mixing libraries, `t.File` and `t.Files`, `fileType` with magic numbers and the security warning. Nothing removed.

Method: documentation only; no commands were run.
