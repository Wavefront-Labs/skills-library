---
id: computing-software.web-development.nestjs.custom-provider-types
name: custom-provider-types
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, providers, dependency-injection, factory, testing]
level: practitioner
status: docs-checked
description: "Register NestJS custom providers with useValue, useClass, useFactory (with inject and optional deps) and useExisting aliases, and export them from modules."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/dependency-injection.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`providers: [CatsService]` is shorthand for `{ provide: CatsService, useClass: CatsService }`. Custom providers let you control the value behind a token.

Value (constants, mocks, external libs):

```typescript
{ provide: CatsService, useValue: mockCatsService }
{ provide: 'CONNECTION', useValue: connection }
```

Class (choose implementation dynamically):

```typescript
const configServiceProvider = {
  provide: ConfigService,
  useClass: process.env.NODE_ENV === 'development'
    ? DevelopmentConfigService : ProductionConfigService,
};
```

Factory (`inject` is positional and entries may be optional):

```typescript
const connectionProvider = {
  provide: 'CONNECTION',
  useFactory: (optionsProvider: MyOptionsProvider, optionalProvider?: string) => {
    const options = optionsProvider.get();
    return new DatabaseConnection(options);
  },
  inject: [MyOptionsProvider, { token: 'SomeOptionalProvider', optional: true }],
};
```

Alias (both tokens resolve to the same singleton):

```typescript
{ provide: 'AliasedLoggerService', useExisting: LoggerService }
```

A provider can supply any value, such as a config object chosen by `NODE_ENV`.

Providers are private to their module. To share, export by token or by the full provider object:

```typescript
@Module({ providers: [connectionFactory], exports: ['CONNECTION'] })
```

Inject non-class tokens with `@Inject('CONNECTION')`.

Gotcha: `useExisting` only shares an instance for singleton scope. Keep tokens in a constants file.

Debugging: set the `NEST_DEBUG` environment variable to get extra dependency resolution logs during startup.

## Checked

2026-11-04. Read the whole custom providers page (`content/fundamentals/dependency-injection.md` in nestjs/docs.nestjs.com). Confirmed the `providers: [CatsService]` shorthand, `useValue`, `useClass`, `useFactory` with positional `inject` and optional entries, `useExisting` (singleton scope), non-service providers, exporting by token or provider object, `@Inject('CONNECTION')`, the constants-file advice and `NEST_DEBUG`. Removed: the "sync or async" factory remark (not on this page) and the invented test-based Verify step.
Method: documentation only; no commands were run.
