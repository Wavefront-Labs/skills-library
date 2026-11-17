---
id: computing-software.web-development.angular.dom-apis-and-renderer
name: dom-apis-and-renderer
category: computing-software
field: web-development
product: angular
tags: [angular, dom, elementref, renderer2, nativeelement, xss, ssr]
level: practitioner
status: docs-checked
description: "When and how to touch the DOM directly in Angular: ElementRef, render callbacks, Renderer2, legitimate use cases and the innerHTML warning."
sources:
  - https://angular.dev/guide/components/dom-apis
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Angular handles most DOM creation, updates and removal. Avoid direct DOM manipulation whenever possible; express structure in templates and update it with bindings.

Get the host element by injecting `ElementRef`:

```ts
@Component(/* ... */)
export class ProfilePhoto {
  constructor() {
    const elementRef = inject(ElementRef);
    afterEveryRender(() => {
      // Focus the first input element in this component.
      elementRef.nativeElement.querySelector('input')?.focus();
    });
  }
}
```

`nativeElement` references the host `Element`. Do DOM work in render callbacks (`afterEveryRender`, `afterNextRender`), which must be called in an injection context such as the constructor and never run during server-side rendering or build-time pre-rendering. Never directly manipulate the DOM in other lifecycle hooks: Angular only guarantees the DOM is fully rendered in render callbacks, and reading or modifying it elsewhere can cause layout thrashing.

`Renderer2`: inject it for manipulations tied to other Angular features.
- Elements created by a component's `Renderer2` participate in that component's style encapsulation.
- `setProperty` updates synthetic animation properties and `listen` adds listeners for synthetic animation events.
- Apart from those two narrow cases it is no different from native DOM APIs. Both work in server-side rendering and pre-rendering, but the server DOM lacks browser-only APIs such as layout measurement and observers.

Legitimate uses of DOM APIs: managing focus, measuring geometry (`getBoundingClientRect`), reading text content, and setting up native observers (`MutationObserver`, `ResizeObserver`, `IntersectionObserver`).

Avoid inserting, removing and modifying elements. Never directly set an element's `innerHTML`: it can expose the app to cross-site scripting. Angular template bindings, including `innerHTML` bindings, include safeguards (see the Angular security guide).

See `computing-software.web-development.angular.after-render-callbacks` for phases.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/dom-apis (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
