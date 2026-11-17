---
id: computing-software.web-development.nestjs.standard-schema-serializer
name: standard-schema-serializer
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, serialization, zod, standard-schema, response-schema]
level: advanced
status: docs-checked
description: "Allowlist and transform NestJS responses with StandardSchemaSerializerInterceptor and a Zod or Valibot schema chosen through SerializeOptions."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application/serialization.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The interceptor runs each handler result through a schema and sends the schema output. Because `z.object()` strips undeclared keys, the schema is an allowlist:

```typescript
export const userResponseSchema = z.object({
  id: z.number(),
  firstName: z.string(),
  lastName: z.string(),
});
```

Bind and select the schema:

```typescript
@Controller('users')
@UseInterceptors(StandardSchemaSerializerInterceptor)
export class UsersController {
  @Get(':id')
  @SerializeOptions({ schema: userResponseSchema })
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.usersService.findOne(id);
  }
}
```

`@SerializeOptions({ schema })` may sit on the class; a handler-level schema wins. When a handler returns an array, the schema is applied to each element, so pass the single-item schema.

Transformations replace `@Expose()` and `@Transform()`:

```typescript
z.object({ id: z.number(), firstName: z.string(), lastName: z.string(), role: z.object({ id: z.number(), name: z.string() }) })
  .transform((user) => ({ id: user.id, fullName: `${user.firstName} ${user.lastName}`, role: user.role.name }));
```

Valibot uses `v.pipe(v.object({...}), v.transform(...))`.

Global binding: `app.useGlobalInterceptors(new StandardSchemaSerializerInterceptor(app.get(Reflector)))`, or register `APP_INTERCEPTOR` and Nest injects `Reflector`. The constructor accepts default `schema` and `validateOptions`.

Gotchas:
- `null`, `undefined`, primitives, `StreamableFile` and handlers with no schema pass through unchanged.
- A response that does not match its schema is a server bug: the client gets `500`, not partial data.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: allowlist behaviour, SerializeOptions schema, array handling, transforms, Valibot form, global binding, constructor options, pass-through cases, 500 on mismatch (serialization page). Removed: invented Verify step.

Method: documentation only; no commands were run.
