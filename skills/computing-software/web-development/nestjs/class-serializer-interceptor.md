---
id: computing-software.web-development.nestjs.class-serializer-interceptor
name: class-serializer-interceptor
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, serialization, classserializerinterceptor, class-transformer, security]
level: practitioner
status: docs-checked
description: "Strip sensitive fields such as passwords from NestJS responses with ClassSerializerInterceptor, Exclude, Expose, Transform and SerializeOptions."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application/serialization.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Annotate the entity with `class-transformer` decorators:

```typescript
export class UserEntity {
  id: number;
  firstName: string;
  lastName: string;

  @Exclude()
  password: string;

  constructor(partial: Partial<UserEntity>) {
    Object.assign(this, partial);
  }
}
```

Apply the interceptor (from `@nestjs/common`) per route or globally:

```typescript
@UseInterceptors(ClassSerializerInterceptor)
@Get()
findOne(): UserEntity {
  return new UserEntity({ id: 1, firstName: 'John', lastName: 'Doe', password: 'password' });
}
```

The response omits `password`. Other decorators: `@Expose()` on a getter adds a computed `fullName`; `@Transform(({ value }) => value.name)` on `role: RoleEntity` returns just the name.

`@SerializeOptions({ excludePrefixes: ['_'] })` forwards options to `instanceToPlain()`. Its `type` option converts plain returns to a class first:

```typescript
@UseInterceptors(ClassSerializerInterceptor)
@SerializeOptions({ type: UserEntity })
@Get()
findOne(): UserEntity { return { id: 1, firstName: 'John', lastName: 'Doe', password: 'password' }; }
```

Gotchas:
- The handler must return a class instance. A plain object such as `{ user: new UserEntity() }` is not serialized correctly.
- With `type`, a returned instance of a different class is treated as a plain object: its own `@Exclude()` is ignored and undeclared properties are copied. Use `@Expose()` on every property plus `excludeExtraneousValues: true` to send only the declared ones.
- `StreamableFile` responses are not serialized.

## Checked

2026-11-04. Read the whole serialization page (`content/application/serialization.md` in nestjs/docs.nestjs.com). Confirmed `@Exclude`, `@Expose` getter, `@Transform`, `ClassSerializerInterceptor` and `SerializeOptions` imports from `@nestjs/common`, options forwarded to `instanceToPlain()`, the `type` option and both warnings, and that `StreamableFile` is not serialized. Nothing removed.
Method: documentation only; no commands were run.
