---
id: computing-software.web-development.nestjs.standard-schema-validation-pipe
name: standard-schema-validation-pipe
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, validation, zod, standard-schema, valibot]
level: advanced
status: docs-checked
description: "Validate requests in NestJS with StandardSchemaValidationPipe and Zod, Valibot or ArkType schemas passed through the schema option of parameter decorators."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application/validation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bind once:

```typescript
app.useGlobalPipes(new StandardSchemaValidationPipe());
```

Define the schema and infer the type:

```typescript
export const createUserSchema = z.object({
  email: z.email(),
  password: z.string().min(8),
  displayName: z.string().max(50).optional(),
});
export type CreateUserDto = z.infer<typeof createUserSchema>;

@Post()
create(@Body({ schema: createUserSchema }) createUserDto: CreateUserDto) {}
```

Only parameters that declare a `schema` are validated, so it can coexist with `ValidationPipe`. `schema` works on `@Body()`, `@Query()`, `@Param()`, `@MessageBody()` and `@Payload()`; pass it after a property name for a single value: `@Body('email', { schema: z.email() })`. Failures give `400` with messages prefixed by path, such as `email: Invalid email address`; array items are prefixed by index (`1.email`).

Coercion and defaults take effect because the handler receives the schema output:

```typescript
@Param('id', { schema: z.coerce.number().int().positive() }) id: number
```

Unknown keys are the schema's decision: `z.object()` strips, `z.strictObject()` rejects, `z.looseObject()` keeps. Derive variants with `.partial()`, `.pick()`, `.omit()`, `.extend()`; arrays with `z.array(schema)`.

Options: `transform` (default `true`; `false` passes the original input, type it with `z.input`), `validateCustomDecorators` (custom `createParamDecorator()` params are skipped unless `true`), `validateOptions`, `errorHttpStatusCode`, `exceptionFactory(issues)` (each issue has `message` and `path` segments that are keys or objects with `key`).

## Checked

2026-11-04. Confirmed against the official NestJS docs source: global binding, schema option and supported decorators, error prefixes, coercion, strict and loose objects, schema composition, pipe options and exceptionFactory (validation page). Removed: invented Verify step.

Method: documentation only; no commands were run.
