---
id: computing-software.web-development.nestjs.guards-canactivate
name: guards-canactivate
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, guards, authorization, canactivate, request-lifecycle]
level: practitioner
status: docs-checked
description: "Write a NestJS guard implementing CanActivate, bind it at method, controller or global scope with UseGuards, and control the denial response."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/guards.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A guard is an `@Injectable()` class implementing `CanActivate`. It decides whether a request reaches the handler, using runtime conditions such as permissions, roles or ACLs. Guards run after all middleware but before any interceptor or pipe, and unlike middleware they know what will execute next through `ExecutionContext`.

```typescript
@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest();
    return validateRequest(request);
  }
}
```

`canActivate()` returns a boolean (sync, Promise or Observable): `true` processes the request, `false` denies it.

Binding:

```typescript
@Controller('cats')
@UseGuards(RolesGuard)   // class: Nest instantiates it, DI works
export class CatsController {}
```

`@UseGuards()` takes one or more guards, at controller or method level, and accepts an instance too (`new RolesGuard()`). Global: `app.useGlobalGuards(new RolesGuard())`, but that cannot inject dependencies because it sits outside any module. To get DI register it in a module:

```typescript
providers: [{ provide: APP_GUARD, useClass: RolesGuard }]
```

The guard is global wherever it is registered. `APP_GUARD` can be registered multiple times; each guard runs for every request in registration order. It is a pseudo-provider, so it cannot be retrieved with `app.get()` or injected.

When a guard returns `false`, Nest throws `ForbiddenException`:

```json
{ "statusCode": 403, "message": "Forbidden resource", "error": "Forbidden" }
```

Throw your own exception (for example `throw new UnauthorizedException();`) for a different response. Exceptions from guards go through the exceptions layer.

Gotcha: in a hybrid application `useGlobalGuards()` does not cover connected microservices by default; in a plain microservice app it does.

Verify: call a route whose guard returns `false`; the response should be the 403 body above (or your thrown exception).

## Checked

2026-11-04. Read the whole guards page (`content/guards.md` in nestjs/docs.nestjs.com). Confirmed `CanActivate`, the middleware and interceptor ordering hint, the return types, `@UseGuards()` forms, `useGlobalGuards()` and its DI limit, `APP_GUARD` and its hints, the hybrid-app notice, the default 403 body and `ForbiddenException`, and exceptions going to the exceptions layer. Reworded the Verify step to what the page states (a `false` return gives the 403 response) and dropped its claim about the handler body.
Method: documentation only; no commands were run.
