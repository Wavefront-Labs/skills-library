---
id: computing-software.web-development.nestjs.feature-shared-global-modules
name: feature-shared-global-modules
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, modules, exports, global, encapsulation]
level: intro
status: docs-checked
description: "Organize NestJS code into feature modules, share providers through exports and re-exports, and use @Global sparingly."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A module is a class with `@Module()`. Its properties: `providers` (instantiated by the injector), `controllers`, `imports` (modules exporting what you need) and `exports` (subset of providers, or tokens, visible to importers). Modules encapsulate providers: you can inject only providers in the same module or exported by an imported module.

Feature module and root wiring:

```typescript
@Module({
  controllers: [CatsController],
  providers: [CatsService],
  exports: [CatsService],
})
export class CatsModule {}

@Module({ imports: [CatsModule] })
export class AppModule {}
```

Modules are singletons, so every importer of `CatsModule` shares one `CatsService` instance. Registering `CatsService` directly in several modules would create separate instances and potentially inconsistent state.

Re-export a module you import so consumers of yours also get it:

```typescript
@Module({ imports: [CommonModule], exports: [CommonModule] })
export class CoreModule {}
```

Module classes can inject providers (for configuration), but a module cannot itself be injected because of circular dependencies.

Make a module global with `@Global()` so its exports are available without importing it. Register global modules once, in the root or core module:

```typescript
@Global()
@Module({ providers: [CatsService], exports: [CatsService] })
export class CatsModule {}
```

Gotcha: global modules reduce boilerplate but hide dependencies; the docs advise against making everything global. Scaffold with `nest g module cats`.

Verify: remove `CatsModule` from `imports` in a consumer module; injecting `CatsService` there should no longer resolve (providers are encapsulated by default) unless the module is `@Global()`, which makes it available without an `imports` entry.

## Checked

2026-11-04. Read the whole modules page (`content/modules.md` in nestjs/docs.nestjs.com). Confirmed the `@Module()` properties, encapsulation, feature and shared modules, singleton sharing, re-exporting, module-class injection limit, `@Global()` and the warning against global modules, and `nest g module`. The Verify step is kept because the page states that a module's providers cannot be used elsewhere without importing it, except for global modules.
Method: documentation only; no commands were run.
