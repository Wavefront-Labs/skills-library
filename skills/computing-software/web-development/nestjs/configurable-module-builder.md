---
id: computing-software.web-development.nestjs.configurable-module-builder
name: configurable-module-builder
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, modules, dynamic-modules, configurablemodulebuilder, async-options]
level: advanced
status: docs-checked
description: "Use ConfigurableModuleBuilder to generate register and registerAsync for a NestJS module, with MODULE_OPTIONS_TOKEN, useFactory, useClass and useExisting."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/dynamic-modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ConfigurableModuleBuilder` builds a module blueprint so you do not hand-write sync and async variants.

```typescript
// id-generator.module-definition.ts
export const { ConfigurableModuleClass, MODULE_OPTIONS_TOKEN } =
  new ConfigurableModuleBuilder<IdGeneratorModuleOptions>().build();

// id-generator.module.ts
@Module({ providers: [IdGenerator], exports: [IdGenerator] })
export class IdGeneratorModule extends ConfigurableModuleClass {}

// consumer
constructor(@Inject(MODULE_OPTIONS_TOKEN) private readonly options: IdGeneratorModuleOptions) {}
```

The class now exposes `register()` and `registerAsync()`:

```typescript
IdGeneratorModule.registerAsync({
  imports: [ConfigModule],
  useFactory: (configService: ConfigService) => ({
    prefix: configService.getOrThrow<string>('USER_ID_PREFIX'),
  }),
  inject: [ConfigService],
})
```

`registerAsync()` accepts `imports`, `useFactory`, `inject`, `useClass`, `useExisting` and `provideInjectionTokensFrom`. Choose exactly one of `useFactory`, `useClass`, `useExisting`. A `useClass` / `useExisting` class must implement `ConfigurableModuleOptionsFactory` (default method `create()`).

Customization on the builder:
- `.setClassMethodName('forRoot')` yields `forRoot()` / `forRootAsync()`.
- `.setFactoryMethodName('createIdGeneratorOptions')` renames the options-factory method.
- `.setExtras({ isGlobal: false }, (definition, extras) => ({ ...definition, global: extras.isGlobal }))` adds options that shape the module but are not placed in `MODULE_OPTIONS_TOKEN`.
- To extend generated methods, export `OPTIONS_TYPE` and `ASYNC_OPTIONS_TYPE` from `build()` and override with `super.register(options)`.

Gotcha: extras such as `isGlobal` are not present on the injected options object.

## Checked

2026-11-04. Read the whole dynamic modules page (`content/fundamentals/dynamic-modules.md` in nestjs/docs.nestjs.com). Confirmed the builder example, `MODULE_OPTIONS_TOKEN`, generated `register()`/`registerAsync()`, every `registerAsync()` property, the exactly-one-of rule, `ConfigurableModuleOptionsFactory` with default `create()`, `setClassMethodName`, `setFactoryMethodName`, `setExtras`, `OPTIONS_TYPE`/`ASYNC_OPTIONS_TYPE` and the extras gotcha. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
