---
id: computing-software.web-development.nestjs.dynamic-module-forroot
name: dynamic-module-forroot
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, modules, dynamic-modules, configuration, forroot]
level: practitioner
status: docs-checked
description: "Build a configurable NestJS dynamic module with a static register or forRoot method returning DynamicModule, an options provider, and re-export or global option."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/modules.md
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/dynamic-modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A dynamic module is configured by its importer at import time. Add a static method (conventionally `register()`, `forRoot()` or `forFeature()`) returning a `DynamicModule`: the same properties as `@Module()` plus `module` (the only required one).

```typescript
@Module({})
export class IdGeneratorModule {
  static register(options: IdGeneratorModuleOptions): DynamicModule {
    return {
      module: IdGeneratorModule,
      providers: [
        { provide: ID_GENERATOR_OPTIONS, useValue: options },
        IdGenerator,
      ],
      exports: [IdGenerator],
    };
  }
}

@Injectable()
export class IdGenerator {
  constructor(
    @Inject(ID_GENERATOR_OPTIONS)
    private readonly options: IdGeneratorModuleOptions,
  ) {}
  generate(): string { return `${this.options.prefix}_${randomUUID()}`; }
}
```

Importing: `imports: [IdGeneratorModule.register({ prefix: 'usr' })]`. Each importer gets its own configured instance.

Convention in `@nestjs/` packages: `register()` configures the module for the calling module only; `forRoot()` configures once and reuses everywhere (one `TypeOrmModule.forRoot()`); `forFeature()` adjusts the root config per module. Async twins are `registerAsync()`, `forRootAsync()`, `forFeatureAsync()`.

Properties returned by the method extend, not override, the `@Module()` metadata. The method may return a Promise. Set `global: true` in the returned object to register globally.

To share one configured instance, import it once in a core module and list the module class (without calling `forRoot()` again) in `exports`.

Gotcha: calling `forRoot()` a second time in another module creates a second, separately configured instance.

## Checked

2026-11-04. Read the whole modules page (`content/modules.md`) and the whole dynamic modules page (`content/fundamentals/dynamic-modules.md`) in nestjs/docs.nestjs.com. Confirmed the `DynamicModule` shape with only `module` required, the `register()` example and options provider, per-importer instances (`usr_` and `ord_`), the `register()`/`forRoot()`/`forFeature()` guidelines and async twins, extend-not-override metadata, Promise return, `global: true`, re-exporting the module class, and the second-`forRoot()` warning. Nothing removed.
Method: documentation only; no commands were run.
