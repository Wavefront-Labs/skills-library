---
id: computing-software.web-development.angular.after-render-effect
name: after-render-effect
category: computing-software
field: web-development
product: angular
tags: [angular, signals, afterrendereffect, dom, phases, third-party-libraries, ssr]
level: advanced
status: docs-checked
description: "Use afterRenderEffect to react to signals after Angular commits DOM updates, with earlyRead, write, mixedReadWrite and read phases and cleanup."
sources:
  - https://angular.dev/guide/signals/effect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`effect` runs before Angular updates the DOM. `afterRenderEffect` works like `effect` but runs after Angular has rendered and committed changes to the DOM; use it to inspect or modify the DOM or integrate third-party libraries needing direct DOM access.

```ts
chartData = input.required<ChartData>();
canvas = viewChild.required<ElementRef<HTMLCanvasElement>>('canvas');
chart: ChartInstance;

constructor() {
  afterNextRender({
    write: () => {
      this.chart = initializeChart(this.canvas().nativeElement, this.chartData());
    },
  });
  afterRenderEffect(() => {
    this.chart.updateData(this.chartData());
  });
}
```

`ResizeObserver`, `MutationObserver` and `IntersectionObserver` are preferred over `effect` or `afterRenderEffect` when possible.

Phases group callbacks to avoid reflows and layout thrashing:
- `earlyRead`: read the DOM before a subsequent write, for example custom layout the browser does not support natively. Prefer `read` if reading can wait.
- `write`: write to the DOM. Never read here.
- `mixedReadWrite`: read and write together. Avoid if work can be divided among other phases.
- `read`: read from the DOM. Never write here.

```ts
afterRenderEffect({
  earlyRead: (cleanupFn) => { /* ... */ },
  write: (previousPhaseValue, cleanupFn) => { /* ... */ },
  mixedReadWrite: (previousPhaseValue, cleanupFn) => { /* ... */ },
  read: (previousPhaseValue, cleanupFn) => { /* ... */ },
});
```

Without phases, callbacks run in `mixedReadWrite`, which may worsen performance through extra reflows. Order is `earlyRead`, `write`, `mixedReadWrite`, `read`. `earlyRead` receives only the cleanup function; each later phase receives the previous phase's return value as a Signal. If a phase modifies a signal tracked by the effect, the affected phases run again. Cleanup callbacks run when the effect is destroyed or before phases re-run.

SSR: like `afterNextRender` and `afterEveryRender`, it only runs on the client, and components are not guaranteed to be hydrated before the callback runs, so be careful reading or writing the DOM and layout directly.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/signals/effect (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
