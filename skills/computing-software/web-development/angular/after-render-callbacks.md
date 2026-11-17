---
id: computing-software.web-development.angular.after-render-callbacks
name: after-render-callbacks
category: computing-software
field: web-development
product: angular
tags: [angular, afternextrender, aftereveryrender, render-callbacks, dom, layout-thrashing, phases]
level: advanced
status: docs-checked
description: "Use afterNextRender and afterEveryRender for manual DOM work, split into earlyRead, write, mixedReadWrite and read phases to avoid layout thrashing."
sources:
  - https://angular.dev/guide/components/lifecycle
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`afterNextRender` runs once the next time all components have been rendered to the DOM; `afterEveryRender` runs every time. They are standalone functions taking a callback, not class methods, and are an application-wide hook not tied to one component instance.

Rules:
- Call them in an injection context, typically a component constructor.
- Use them for manual DOM operations.
- They do not run during server-side rendering or build-time pre-rendering.

You can split the work into phases. Phases let you sequence writes before reads to minimize layout thrashing; a phase function may return a value that the next phase receives.

```ts
constructor() {
  const nativeElement = inject(ElementRef).nativeElement;

  afterNextRender({
    // Write phase: write to a geometric property.
    write: () => {
      const padding = computePadding();
      const changed = padding !== this.prevPadding;
      if (changed) {
        nativeElement.style.padding = padding;
      }
      return changed; // passed to the read phase
    },
    // Read phase: read geometry after all writes.
    read: (didWrite) => {
      if (didWrite) {
        this.elementHeight = nativeElement.getBoundingClientRect().height;
      }
    },
  });
}
```

Four phases run in this order:
1. `earlyRead`: read layout-affecting DOM properties and styles strictly necessary for subsequent calculation. Avoid if possible, preferring `write` and `read`.
2. `write`: write layout-affecting DOM properties and styles.
3. `mixedReadWrite`: the default phase, for operations needing both. Avoid if possible, preferring explicit `write` and `read`.
4. `read`: read layout-affecting DOM properties.

On initialization the order is change detection hooks, then `afterNextRender`, then `afterEveryRender`; on later updates only `afterEveryRender` runs. See `computing-software.web-development.angular.component-lifecycle-hooks` for the other hooks.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/components/lifecycle (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
