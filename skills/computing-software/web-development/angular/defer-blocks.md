---
id: computing-software.web-development.angular.defer-blocks
name: defer-blocks
category: computing-software
field: web-development
product: angular
tags: [angular, defer, lazy-loading, defer-block, placeholder, loading, error, bundle-size]
level: practitioner
status: docs-checked
description: "Deferrable views with @defer: which dependencies are deferred, and the @placeholder, @loading and @error sub-blocks with minimum and after timers."
sources:
  - https://angular.dev/guide/templates/defer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`@defer` splits the code of components, directives, pipes and component CSS inside it into a separate JavaScript file, loaded after the rest of the template renders. This reduces initial bundle size and can improve Core Web Vitals (LCP, TTFB).

```html
@defer {
  <large-component />
}
```

Conditions for a dependency to be deferred:
1. It must be standalone. Non-standalone dependencies stay eager, even inside `@defer` (transitive dependencies may still be in an `NgModule`).
2. It must not be referenced outside `@defer` blocks in the same file, nor in `ViewChild` queries; otherwise it is eagerly loaded.

The compiler emits a dynamic import per dependency; the block renders after all imports resolve, in no guaranteed order. By default a block triggers when the browser is idle.

Sub-blocks:
- `@placeholder`: optional content shown before the trigger. Its dependencies are eagerly loaded. Takes `minimum` time (`ms` or `s`) to avoid flicker: `@placeholder (minimum 500ms) { <p>Placeholder content</p> }`. Some triggers need a placeholder or a template reference variable.
- `@loading`: optional content shown while dependencies load, replacing the placeholder. Eagerly loaded dependencies. Parameters `after` (wait after loading begins before showing) and `minimum` (minimum display time), both `ms` or `s`, timers starting when loading is triggered: `@loading (after 100ms; minimum 1s) { <img alt="loading..." src="loading.gif" /> }`.
- `@error`: optional content when deferred loading fails; its dependencies are eagerly loaded too.

```html
@defer {
  <large-component />
} @loading {
  <img alt="loading..." src="loading.gif" />
} @placeholder {
  <p>Placeholder content</p>
} @error {
  <p>Failed to load large component.</p>
}
```

`@defer` works with both standalone and NgModule-based components, but only standalone components, directives and pipes can be deferred. Triggers and prefetching: `computing-software.web-development.angular.defer-triggers`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/templates/defer (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
