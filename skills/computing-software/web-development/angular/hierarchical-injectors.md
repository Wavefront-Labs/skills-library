---
id: computing-software.web-development.angular.hierarchical-injectors
name: hierarchical-injectors
category: computing-software
field: web-development
product: angular
tags: [angular, di, elementinjector, environmentinjector, self, skipself, host, optional]
level: advanced
status: docs-checked
description: "Angular hierarchical DI: ElementInjector versus EnvironmentInjector, two-phase resolution, optional self skipSelf host modifiers, providers versus viewProviders."
sources:
  - https://angular.dev/guide/di/hierarchical-dependency-injection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two hierarchies:
- `EnvironmentInjector`: configured with `@Service()` or the `ApplicationConfig` `providers` array. `@Service()` is preferred because it can be tree-shaken. `bootstrapApplication()` creates the root `EnvironmentInjector` as a child of the platform injector; above that sits `NullInjector()`, which throws unless the request is optional (then `null`). The Router creates child `EnvironmentInjector`s for dynamically loaded components. An `ApplicationConfig` provider overrides one configured for `root`, e.g. `{provide: LocationStrategy, useClass: HashLocationStrategy}`.
- `ElementInjector`: created implicitly per DOM element, empty unless configured via `providers` or `viewProviders` on `@Directive()` or `@Component()`. Components and directives on the same element share an injector. A service provided in a component is destroyed with that instance.

Resolution: first against parents in the `ElementInjector` hierarchy, then against the `EnvironmentInjector` hierarchy; if still not found, an error is thrown. The first provider found for a token wins.

Modifiers, passed to `inject()`:
- `optional: true`: resolve `null` instead of throwing.
- `self: true`: look only at the current element's injector (combine with `optional` to avoid errors).
- `skipSelf: true`: start at the parent injector, ignoring the current one.
- `host: true`: stop the search at the host component's view.
Combinations not allowed: `host` with `self`, and `skipSelf` with `self`.

```ts
leaf = inject(LeafService, {optional: true, self: true});
parent = inject(Person, {optional: true, skipSelf: true});
```

Constructor equivalents: `@Optional()`, `@Self()`, `@SkipSelf()`, `@Host()`.

`providers` versus `viewProviders`: `viewProviders` are visible only inside the component's own view; content projected with `<ng-content>` cannot see them. Angular DI tracks where a component was declared, not where it renders. To give projected content access, take it as a template and render it with an explicit injector:

```ts
@Component({
  viewProviders: [AnimalService],
  imports: [NgTemplateOutlet],
  template: `<ng-container [ngTemplateOutlet]="content()" [ngTemplateOutletInjector]="injector" />`,
})
export class Child {
  readonly content = contentChild.required(TemplateRef);
  readonly injector = inject(Injector);
}
```

Use cases: isolate a service by providing it only in one component (`providers: [VillainsService]`), give each component instance its own state (a `@Service({autoProvided: false})` class listed in the component's `providers`), or substitute a more specialised implementation deeper in the tree.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/di/hierarchical-dependency-injection (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
