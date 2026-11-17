---
id: computing-software.web-development.nestjs.circular-dependencies-forwardref
name: circular-dependencies-forwardref
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, circular-dependency, forwardref, modules, providers]
level: advanced
status: docs-checked
description: "Resolve circular dependencies between NestJS providers and modules with forwardRef and Inject, or break them with ModuleRef, and avoid barrel files."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/circular-dependency.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A circular dependency means A needs B and B needs A, between providers or modules. Avoid them where possible; where you cannot, use `forwardRef()` from `@nestjs/common` on both sides.

Providers:

```typescript
@Injectable()
export class CatsService {
  constructor(
    @Inject(forwardRef(() => CommonService))
    private commonService: CommonService,
  ) {}
}

@Injectable()
export class CommonService {
  constructor(
    @Inject(forwardRef(() => CatsService))
    private catsService: CatsService,
  ) {}
}
```

Modules (both sides again):

```typescript
@Module({ imports: [forwardRef(() => CatsModule)] })
export class CommonModule {}

@Module({ imports: [forwardRef(() => CommonModule)] })
export class CatsModule {}
```

Alternative: refactor and use `ModuleRef` to fetch the provider on one side lazily, so no constructor cycle exists.

In plain JavaScript use `@Dependencies(forwardRef(() => CommonService))`.

Gotchas:
- Instantiation order is indeterminate. Your code must not depend on which constructor runs first.
- Circular dependencies involving `Scope.REQUEST` providers can lead to undefined dependencies (a linked GitHub issue is cited).
- Barrel files (`index.ts`) can create accidental cycles. Do not use barrels for module and provider classes, and never import a sibling via the barrel in the same directory (`cats/cats.controller` should not import `cats` to reach `cats/cats.service`).

## Checked

2026-11-04. Read the whole circular dependency page (`content/fundamentals/circular-dependency.md` in nestjs/docs.nestjs.com). Confirmed the `forwardRef()` provider and module examples (both sides), `@Dependencies` for JavaScript, the `ModuleRef` alternative, the indeterminate-order and `Scope.REQUEST` warning, and the barrel-file warning. Removed: the claim that a module class cannot be injected as a provider, and the Verify step with its startup error description (neither is on the page).
Method: documentation only; no commands were run.
