---
id: computing-software.web-development.angular.injection-tokens
name: injection-tokens
category: computing-software
field: web-development
product: angular
tags: [angular, di, injectiontoken, factory, providedin, interface]
level: practitioner
status: docs-checked
description: "InjectionToken in Angular: tokens for non-class values, root-provided tokens with a factory, browser API tokens, and why interfaces cannot be tokens."
sources:
  - https://angular.dev/guide/di/defining-dependency-providers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An `InjectionToken` is the unique key Angular DI uses to store and retrieve any value (strings, functions, config objects).

```ts
export const API_URL = new InjectionToken<string>('api.url');
export const LOGGER = new InjectionToken<(msg: string) => void>('logger.function');
```

The string is a debugging description only; Angular identifies tokens by object reference.

A token with a `factory` is `providedIn: 'root'` by default (overridable via `providedIn`), needs no `providers` entry, is tree-shakeable and type-safe, and the factory can call `inject()`:

```ts
export const APP_CONFIG = new InjectionToken<AppConfig>('app.config', {
  providedIn: 'root',
  factory: () => ({apiUrl: 'https://api.example.com', version: '1.0.0', features: {darkMode: true}}),
});

export const LOGGER_FN = new InjectionToken<LoggerFn>('logger.function', {
  providedIn: 'root',
  factory: () => {
    const config = inject(APP_CONFIG);
    return (level: string, message: string) => { /* use config */ };
  },
});

export const LOCAL_STORAGE = new InjectionToken<Storage>('localStorage', {
  factory: () => window.localStorage,
});
```

Interfaces cannot be injection identifiers because they do not exist at runtime. Use a token typed with the interface:

```ts
export const DATA_SERVICE_TOKEN = new InjectionToken<DataService>('DataService');

@Component({ providers: [{provide: DATA_SERVICE_TOKEN, useClass: LocalDataService}] })
export class Example { private dataService = inject(DATA_SERVICE_TOKEN); }
```

TypeScript types and interfaces also cannot serve as `useValue` values, since they exist only at compile time.

Use tokens when you cannot use a class, or want several implementations of one interface.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/di/defining-dependency-providers (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page. Removed a cross-reference to another skill that the page does not make.
