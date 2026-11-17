---
id: computing-software.web-development.angular.content-projection
name: content-projection
category: computing-software
field: web-development
product: angular
tags: [angular, ng-content, content-projection, slots, ngprojectas, fallback-content]
level: practitioner
status: docs-checked
description: "Project content into components with ng-content: multiple select slots, catch-all, fallback content, ngProjectAs, and change detection and DI caveats."
sources:
  - https://angular.dev/guide/components/content-projection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`<ng-content>` marks where children of a component's host element render (are projected). It works like the native `<slot>` element with extra Angular features.

```ts
@Component({
  selector: 'custom-card',
  template: `
    <div class="card-shadow">
      <ng-content select="card-title">Default Title</ng-content>
      <div class="card-divider"></div>
      <ng-content />
    </div>`,
})
export class CustomCard {}
```

Rules:
- `<ng-content>` is neither a component nor a DOM element; it is processed at build time. You cannot insert, remove or modify it at run time, or add directives, styles or arbitrary attributes to it.
- Do not conditionally include `<ng-content>` with `@if`, `@for` or `@switch`: Angular always instantiates DOM nodes for projected content even if the placeholder is hidden. For conditional content see template fragments (`ng-template`).
- `select` accepts the same CSS selectors as component selectors. A placeholder without `select` captures everything that did not match another. If none exists, unmatched elements do not render.
- Fallback content is whatever you put inside the `<ng-content>` element, shown when no matching content is provided.
- `ngProjectAs` on any element makes Angular compare its value, not the element identity, against `select`: `<h3 ngProjectAs="card-title">Hello</h3>`. It supports only static values.

Caveats:
- Projected content belongs to the parent's view. Change detection checks it when the parent runs, so an `OnPush` wrapper does not skip it.
- Projected content gets dependencies from the parent's injector, not the receiving component's `viewProviders`.
- Library components such as menus, tabs and lists that use `ContentChildren` may break (keyboard navigation, ARIA) when children are wrapped and projected; check their docs first.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/content-projection (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
