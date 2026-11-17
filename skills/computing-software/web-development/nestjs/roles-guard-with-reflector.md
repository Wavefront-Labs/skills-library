---
id: computing-software.web-development.nestjs.roles-guard-with-reflector
name: roles-guard-with-reflector
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, guards, reflector, metadata, rbac]
level: practitioner
status: docs-checked
description: "Build a role-based NestJS guard using Reflector.createDecorator or SetMetadata and merge handler and controller metadata with getAllAndOverride."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/guards.md
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/execution-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Attach metadata to handlers with a typed decorator, then read it in a guard through `Reflector` (from `@nestjs/core`).

```typescript
// roles.decorator.ts
export const Roles = Reflector.createDecorator<string[]>();

@Post()
@Roles(['admin'])
async create(@Body() createCatDto: CreateCatDto) {}

// roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.get(Roles, context.getHandler());
    if (!roles) return true;
    const request = context.switchToHttp().getRequest();
    const user = request.user;
    return matchRoles(roles, user.roles);
  }
}
```

`matchRoles()` is your function, not Nest's. The guard assumes `request.user` was attached earlier by an authentication step.

Low-level alternative with a string key:

```typescript
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);
const roles = this.reflector.get<string[]>('roles', context.getHandler());
```

Prefer a wrapper decorator over using `@SetMetadata()` directly in routes.

Metadata can sit on the controller too; read it with `context.getClass()`. When both levels exist:

- `getAllAndOverride(Roles, [context.getHandler(), context.getClass()])` returns the first defined value, so `@Roles(['user'])` on the class and `@Roles(['admin'])` on the method yields `['admin']`.
- `getAllAndMerge(Roles, [context.getHandler(), context.getClass()])` merges arrays or objects in target order, yielding `['admin', 'user']`.

Gotcha: a guard that reads only `getHandler()` ignores class-level metadata; pass both targets as above.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: Reflector.createDecorator, SetMetadata form, getAllAndOverride and getAllAndMerge results, matchRoles note, request.user assumption (guards and execution-context pages). Removed: invented Verify step.

Method: documentation only; no commands were run.
