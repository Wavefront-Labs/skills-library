---
id: computing-software.web-development.angular.creating-services
name: creating-services
category: computing-software
field: web-development
product: angular
tags: [angular, di, service, injectable, inject, factory, autoprovided]
level: intro
status: docs-checked
description: "Create and inject Angular services: the Service decorator versus Injectable, root singletons, factory option, autoProvided false, and inject() in components."
sources:
  - https://angular.dev/guide/di/creating-and-using-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generate with `ng generate service CUSTOM_NAME`, or add the `@Service()` decorator to a class by hand.

```ts
import {Service} from '@angular/core';

@Service()
export class BasicDataStore {
  private data: string[] = [];
  addData(item: string): void { this.data.push(item); }
  getData(): string[] { return [...this.data]; }
}
```

Services are provisioned at the root level by default, which gives: a single shared instance for the whole app, global availability without manual provider registration, and tree-shakability (excluded from the production bundle if never used).

`@Service` is shorthand for `@Injectable({ providedIn: 'root' })`.

| Requirement | `@Service` | `@Injectable` |
| --- | --- | --- |
| `inject()` function | Yes | Yes |
| Constructor-based DI | No | Yes |
| Implicit root singleton | Yes | No (needs `{providedIn: 'root'}`) |
| `useClass` and other advanced provider keys | No | Yes |
| Custom initialization factories | Yes | Yes |
| Non-root scopes such as `platform` | No | Yes |

Use `@Service` for a new singleton class that uses `inject()`. Keep `@Injectable` for constructor injection, `useClass`/`useValue`/`useExisting`/`useFactory`, or non-root scopes.

Factory: pass `factory` to control creation, for example swapping implementations per environment. It runs in an injection context, so `inject()` works inside it. It replaces `useClass`, `useValue`, `useExisting` and `useFactory`.

```ts
@Service({
  factory: () => (inject(ANALYTICS_ENABLED) ? new GoogleAnalytics() : new Analytics()),
})
export class Analytics { track(event: string, payload?: Record<string, unknown>) {} }
```

Opt out of root provisioning with `@Service({autoProvided: false})`; you must then add it to a `providers` array yourself, for example to scope it to a route or component.

Inject with `inject()` from `@angular/core`, in a component (`dataStore = inject(BasicDataStore);`) or in another service (`private advancedDataStore = inject(AdvancedDataStore);`).

Next: `computing-software.web-development.angular.di-providers`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/di/creating-and-using-services (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
