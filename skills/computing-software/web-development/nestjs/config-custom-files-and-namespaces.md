---
id: computing-software.web-development.nestjs.config-custom-files-and-namespaces
name: config-custom-files-and-namespaces
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, configuration, registeras, namespaces, configtype]
level: practitioner
status: docs-checked
description: "Structure NestJS config with factory files, registerAs namespaces, typed injection via ConfigType, asProvider, forFeature, and conditional modules."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Custom configuration file: export a factory returning any nested object; load via `load: [configuration]`.

```typescript
export default () => ({
  port: parseInt(process.env.PORT ?? '', 10) || 3000,
  database: { host: process.env.DATABASE_HOST, port: parseInt(process.env.DATABASE_PORT ?? '', 10) || 5432 },
});
```

Read with dot paths: `configService.get<string>('database.host')`, or the whole object via an interface `get<DatabaseConfig>('database')`. YAML works the same way (parse with `js-yaml` inside the factory) but the Nest CLI does not copy non-TS assets: add them under `compilerOptions.assets` in `nest-cli.json`. Files are not validated by `validationSchema`; throw from the factory instead.

Namespaces:

```typescript
export default registerAs('database', () => ({
  host: process.env.DATABASE_HOST,
  port: process.env.DATABASE_PORT || 5432,
}));
```

Inject with strong typing:

```typescript
constructor(
  @Inject(databaseConfig.KEY)
  private dbConfig: ConfigType<typeof databaseConfig>,
) {}
```

Feed another module's async options: `TypeOrmModule.forRootAsync(databaseConfig.asProvider())`. That returns `{ imports: [ConfigModule.forFeature(databaseConfig)], useFactory, inject: [databaseConfig.KEY] }`.

Partial registration: `imports: [ConfigModule.forFeature(databaseConfig)]` in a feature module.

Conditional modules: `ConditionalModule.registerWhen(FooModule, 'USE_FOO')` loads the module unless the variable is `false` (case-insensitive); pass a function `(env) => !!env['foo'] && !!env['bar']` for custom logic. `ConfigModule` must also be loaded; the hook times out after 5 seconds by default.

Gotcha: values loaded by `forFeature()` may not exist yet in a constructor because module init order is indeterminate; read them in `onModuleInit()`.

## Checked

2026-11-04. Read the whole configuration page (`content/application/configuration.md` in nestjs/docs.nestjs.com). Confirmed the factory file and `load`, dot-path `get`, the interface hint, the YAML/`js-yaml` flow and `nest-cli.json` assets note, no `validationSchema` for config files, `registerAs`, `ConfigType` injection, `asProvider()` return shape, `forFeature()`, `ConditionalModule.registerWhen` (case-insensitive `false`, function condition, 5 second hook timeout) and the `onModuleInit()` warning. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
