---
id: computing-software.web-development.nestjs.module-ref-get-resolve-create
name: module-ref-get-resolve-create
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, moduleref, dependency-injection, scopes, dynamic-instantiation]
level: advanced
status: docs-checked
description: "Use NestJS ModuleRef to get static providers, resolve scoped providers with context ids, and instantiate unregistered classes at runtime."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/module-reference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inject `ModuleRef` (from `@nestjs/core`) to look up providers by token outside normal constructor injection.

```typescript
@Injectable()
export class CatsService implements OnModuleInit {
  private service: Service;
  constructor(private moduleRef: ModuleRef) {}

  onModuleInit() {
    this.service = this.moduleRef.get(Service);
  }
}
```

`get()` finds a provider, controller or injectable (guard, interceptor) in the current module and throws if absent. To look across modules use `this.moduleRef.get(Service, { strict: false })`. It cannot retrieve transient or request-scoped providers (including implicitly request-scoped ones).

For scoped providers use `resolve()`, which returns a unique instance from its own DI sub-tree. Each call gets a different instance unless you share a context id:

```typescript
const contextId = ContextIdFactory.create();
const [a, b] = await Promise.all([
  this.moduleRef.resolve(TransientService, contextId),
  this.moduleRef.resolve(TransientService, contextId),
]);
console.log(a === b); // true; without contextId it is false
```

Manually created context ids have an `undefined` `REQUEST` provider. Register one with `this.moduleRef.registerRequestByContextId(/* YOUR_REQUEST_OBJECT */, contextId)`.

Inside a request-scoped class, reuse the current request's sub-tree:

```typescript
constructor(@Inject(REQUEST) private request: Record<string, unknown>) {}
const contextId = ContextIdFactory.getByRequest(this.request);
const catsRepository = await this.moduleRef.resolve(CatsRepository, contextId);
```

To instantiate a class that was never registered as a provider:

```typescript
this.catsFactory = await this.moduleRef.create(CatsFactory);
```

Gotcha: `resolve()` is async while `get()` is sync; mixing them up returns a promise where an instance is expected.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: get() with strict false, scoped-provider limits, resolve() and context ids, registerRequestByContextId, getByRequest, create() (module-reference page). Removed: forwardRef() alternative claim (not on the page); invented Verify step.

Method: documentation only; no commands were run.
