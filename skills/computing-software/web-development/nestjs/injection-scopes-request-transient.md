---
id: computing-software.web-development.nestjs.injection-scopes-request-transient
name: injection-scopes-request-transient
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, scopes, request-scoped, transient, inquirer]
level: practitioner
status: docs-checked
description: "Choose between DEFAULT, REQUEST and TRANSIENT NestJS provider scopes, inject REQUEST or INQUIRER, and understand scope bubbling and performance cost."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/provider-scopes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scopes: `DEFAULT` (one shared instance, created at bootstrap), `REQUEST` (new instance per request, garbage-collected afterwards) and `TRANSIENT` (a new dedicated instance for each consumer that injects it).

```typescript
@Injectable({ scope: Scope.REQUEST })
export class CatsService {}

{ provide: 'CACHE_MANAGER', useClass: CacheManager, scope: Scope.TRANSIENT }

@Controller({ path: 'cats', scope: Scope.REQUEST })
export class CatsController {}
```

`REQUEST` scope bubbles up the injection chain: with `CatsController <- CatsService <- CatsRepository`, a request-scoped `CatsService` makes the controller request-scoped, while `CatsRepository` stays singleton. Transient does not bubble: a singleton that injects a transient gets one fresh transient instance and stays singleton.

Access the raw request with the inherently request-scoped `REQUEST` token (from `@nestjs/core`):

```typescript
constructor(@Inject(REQUEST) private request: Request) {}
```

In GraphQL inject `CONTEXT` from `@nestjs/graphql` and configure `context` to contain `request`.

To learn which class constructed a provider (logging, metrics), inject `INQUIRER` into a transient provider:

```typescript
@Injectable({ scope: Scope.TRANSIENT })
export class HelloService {
  constructor(@Inject(INQUIRER) private parentClass: object) {}
}
```

Gotchas: request scope makes Nest instantiate classes on every request; the docs say a well-designed app should see no more than about 5% latency increase, and singleton is recommended. Passport strategies and Cron controllers should not be request-scoped. To pass per-request values like the user or tenant without changing scopes, an AsyncLocalStorage store keeps providers singletons.

## Checked

2026-11-04. Read the whole injection scopes page (`content/fundamentals/provider-scopes.md` in nestjs/docs.nestjs.com). Confirmed the three scopes, `@Injectable`, custom-provider and `@Controller` scope syntax, scope bubbling and the transient exception, `REQUEST`, `CONTEXT` and `INQUIRER`, the ~5% latency hint, the Passport and Cron notice and the AsyncLocalStorage remark. Removed: "lifecycle hooks are not called for request-scoped classes" (not on this page) and the invented constructor-logging Verify step.
Method: documentation only; no commands were run.
