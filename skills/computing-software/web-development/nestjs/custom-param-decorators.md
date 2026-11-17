---
id: computing-software.web-development.nestjs.custom-param-decorators
name: custom-param-decorators
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, decorators, createparamdecorator, applydecorators, request]
level: practitioner
status: docs-checked
description: "Create NestJS custom parameter decorators with createParamDecorator, pass data, apply pipes, and compose decorators with applyDecorators."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/custom-decorators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replace repetitive `req.user` access with a param decorator:

```typescript
export const User = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    return data ? user?.[data] : user;
  },
);

@Get()
async findOne(@User() user: UserEntity) {}

@Get()
async hello(@User('firstName') firstName: string) {}
```

The `data` argument is whatever is passed to the decorator. `createParamDecorator<T>()` is generic; omit types and `data` is `any`.

Pipes run on custom decorator params like built-in ones. `ValidationPipe` skips them by default, so enable it:

```typescript
@User(new ValidationPipe({ validateCustomDecorators: true })) user: UserEntity
```

A Standard Schema can be attached with `@User('email', { schema: z.email() })`, validated by a `StandardSchemaValidationPipe` with `validateCustomDecorators` enabled.

Combine decorators with `applyDecorators()`:

```typescript
export function Auth(...roles: Role[]) {
  return applyDecorators(
    SetMetadata('roles', roles),
    UseGuards(AuthGuard, RolesGuard),
    ApiBearerAuth(),
    ApiUnauthorizedResponse({ description: 'Unauthorized' }),
  );
}

@Get('users')
@Auth('admin')
findAllUsers() {}
```

Gotcha: `@ApiHideProperty()` from `@nestjs/swagger` is not composable and does not work correctly inside `applyDecorators()`. The `request.user` value must already be attached by an auth step.

## Checked

2026-11-04. Read the whole custom route decorators page (`content/custom-decorators.md` in nestjs/docs.nestjs.com). Confirmed the `@User()` decorator and `data` argument, the generic `createParamDecorator<T>()` hint, pipes on custom decorators and `validateCustomDecorators`, the `schema` option with `StandardSchemaValidationPipe`, `applyDecorators()` and the `@ApiHideProperty()` warning. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
