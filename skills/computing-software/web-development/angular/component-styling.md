---
id: computing-software.web-development.angular.component-styling
name: component-styling
category: computing-software
field: web-development
product: angular
tags: [angular, component, styles, view-encapsulation, shadow-dom, ng-deep, host]
level: practitioner
status: docs-checked
description: "Angular component styles, the four ViewEncapsulation modes, ::ng-deep behavior, style elements in templates and external style references."
sources:
  - https://angular.dev/guide/components/styling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Component styles go in `styles` (inline) or `styleUrl` (file). They are emitted with the component's JavaScript, so Angular includes them whenever the component renders, even when lazy-loaded. Any tool that outputs CSS (Sass, Less, Stylus) works.

Set the scoping mode in the decorator:

```ts
@Component({
  /* ... */
  encapsulation: ViewEncapsulation.None,
})
```

Modes:
- `Emulated` (default): Angular adds a unique generated attribute to template elements and to your style selectors, so component styles do not leak out. Global styles may still affect the component. `:host` and `:host-context()` work without native Shadow DOM, since the compiler turns them into attributes; `::shadow` and `::part` are not supported.
- `ShadowDom`: uses the native Shadow DOM API; Angular attaches a shadow root to the host and renders template and styles in it. It also affects event propagation, `<slot>` interaction and dev tools display.
- `ExperimentalIsolatedShadowDom`: like ShadowDom, but strictly guarantees only the component's styles apply to its template elements.
- `None`: no encapsulation; the component's styles behave as global styles.

In `Emulated` and `ShadowDom`, Angular does not guarantee your styles override outside styles; same specificity is assumed.

`::ng-deep` (strongly discouraged for new use, kept for backwards compatibility): after it in a selector, encapsulation boundaries stop applying.
- `::ng-deep p a` matches `<a>` under `<p>` anywhere in the app (effectively global).
- `p ::ng-deep a` requires `<p>` from the component's template; `<a>` may be anywhere in the application (the component's template, or projected or child content).
- `:host ::ng-deep p a` requires both under the host element.

Other rules: a `<style>` element in a template follows the component's encapsulation mode, but bindings inside it are not supported. `<link>` references and CSS `@import` are treated as external styles and are not affected by emulated encapsulation.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/styling (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
Reworded the `p ::ng-deep a` bullet to match the page (the `<a>` may be anywhere in the application).

Method: documentation only; no commands were run.
