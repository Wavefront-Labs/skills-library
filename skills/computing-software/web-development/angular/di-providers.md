---
id: computing-software.web-development.angular.di-providers
name: di-providers
category: computing-software
field: web-development
product: angular
tags: [angular, di, providers, useclass, usevalue, usefactory, useexisting, multi]
level: practitioner
status: docs-checked
description: "Angular provider configuration: provide with useClass, useValue, useFactory, useExisting, deps and multi providers, and where to register providers."
sources:
  - https://angular.dev/guide/di/defining-dependency-providers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Think of DI as a dictionary: `provide` is the key (a class or `InjectionToken`), and one `use*` key defines the value. The shorthand `providers: [LocalService]` equals `{provide: LocalService, useClass: LocalService}`.

- `useClass`: provides a class; may be a different implementation, even conditional: `{provide: StorageService, useClass: environment.production ? CloudStorageService : LocalStorageService}`.
- `useValue`: any static value: `{provide: MAX_RETRIES_TOKEN, useValue: 3}`.
- `useFactory`: a function returning the value, with dependencies in `deps`:

```ts
{provide: LoggerService, useFactory: loggerFactory, deps: [APP_CONFIG]}
// optional dep
deps: [RequiredService, [new Optional(), OptionalService]]
```

A factory can instead call `inject()` itself (for example `const http = inject(HttpClient);`) and be used as `{provide: ApiClient, useFactory: apiClientFactory}`.
- `useExisting`: an alias; both tokens return the same instance: `[NewLogger, {provide: OldLogger, useExisting: NewLogger}]`. Do not confuse it with `useClass`, which creates separate instances.

Multi providers: `multi: true` collects contributions into an array for one token.

```ts
{provide: INTERCEPTOR_TOKEN, useClass: AuthInterceptor, multi: true},
{provide: INTERCEPTOR_TOKEN, useClass: LoggingInterceptor, multi: true},
```

Services without `providedIn` must be provided manually, e.g. `providers: [LocalDataStore]` on a component. Providing a root service in a component's `providers` creates a new instance tied to that component's life and destroyed with it.

Where to provide:
- Application bootstrap (`bootstrapApplication(App, {providers: [...]})`): global singletons, global configuration, or `provideSomething` functions and providers with side effects. Drawbacks: always in the bundle even if never injected, hard to customise per feature.
- Component or directive `providers`: isolated instances and component-specific state. Drawbacks: a new instance per component, always bundled with the component. If several directives on one element provide the same token, which wins is undefined.
- Route `providers`: available to all components, directives, guards and resolvers in that route, but instantiated independently of the route's components, so they have no route-specific information.

Library pattern: export a `provideX(config): Provider[]` function that keeps internal tokens private, e.g. `return [{provide: ANALYTICS_CONFIG, useValue: config}, AnalyticsService];`, and compose optional `with*()` feature functions.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/di/defining-dependency-providers (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
