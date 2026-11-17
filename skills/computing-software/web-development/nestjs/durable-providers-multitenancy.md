---
id: computing-software.web-development.nestjs.durable-providers-multitenancy
name: durable-providers-multitenancy
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, scopes, durable-providers, multi-tenancy, contextidstrategy]
level: sme
status: docs-checked
description: "Reduce multi-tenant request-scope overhead in NestJS with durable providers and a ContextIdStrategy that maps requests to shared per-tenant DI sub-trees."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/provider-scopes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Problem: a request-scoped data-source provider that reads a tenant header makes most of the app implicitly request-scoped. Durable providers share one DI sub-tree per tenant instead of rebuilding it for every request.

1. Register a `ContextIdStrategy`:

```typescript
const tenants = new Map<string, ContextId>();

export class AggregateByTenantContextIdStrategy implements ContextIdStrategy {
  attach(contextId: ContextId, request: Request) {
    const tenantId = request.headers['x-tenant-id'] as string;
    let tenantSubTreeId: ContextId;
    if (tenants.has(tenantId)) {
      tenantSubTreeId = tenants.get(tenantId);
    } else {
      tenantSubTreeId = ContextIdFactory.create();
      tenants.set(tenantId, tenantSubTreeId);
    }
    // If tree is not durable, return the original "contextId" object
    return (info: HostComponentInfo) =>
      info.isTreeDurable ? tenantSubTreeId : contextId;
  }
}
```

To expose a payload to `@Inject(REQUEST)` (or `CONTEXT` in GraphQL) return `{ resolve: (info) => ..., payload: { tenantId } }` instead.

2. Apply it before any request arrives, e.g. in `main.ts`:

```typescript
ContextIdFactory.apply(new AggregateByTenantContextIdStrategy());
```

3. Flag the providers: `@Injectable({ scope: Scope.REQUEST, durable: true })`, or for custom providers `scope: Scope.REQUEST, durable: true`.

Durability bubbles up like request scope: A depends on durable B, so A is durable if all its other request-scoped dependencies are durable too. Nest reads the `durable` flag only from providers explicitly declared `Scope.REQUEST`.

Gotchas: the docs warn this strategy is not ideal for applications with a large number of tenants. Register the strategy before any request hits the application, or it will not work as intended. Imports `ContextIdFactory`, `ContextId`, `ContextIdStrategy`, `HostComponentInfo` come from `@nestjs/core`.

## Checked

2026-11-04. Read the whole injection scopes page (`content/fundamentals/provider-scopes.md` in nestjs/docs.nestjs.com), including the Durable providers section. Confirmed the multi-tenant problem, the `ContextIdStrategy` code, the payload variant, `ContextIdFactory.apply()` and its timing, the `durable: true` flag on `Scope.REQUEST` providers (class and custom), durability bubbling, the large-tenant warning and the `@nestjs/core` imports. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
