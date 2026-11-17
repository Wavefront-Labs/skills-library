---
id: computing-software.web-development.angular.lazy-loading-services
name: lazy-loading-services
category: computing-software
field: web-development
product: angular
tags: [angular, di, injectasync, lazy-loading, prefetch, onidle, code-splitting]
level: advanced
status: docs-checked
description: "Load Angular services on demand with injectAsync: dynamic import chunks, default exports, onIdle prefetch with timeout and custom PrefetchTrigger functions."
sources:
  - https://angular.dev/guide/di/lazy-loading-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`injectAsync` loads a service only when needed, useful when a service depends on a large library or rarely used feature. The bundler splits the service into a separate chunk downloaded the first time you ask for the instance; afterwards Angular resolves it through regular DI, so it can depend on other injectables and behaves like any singleton.

The service must be auto-provided: decorate it with `@Injectable({providedIn: 'root'})` or `@Service()`. Otherwise Angular cannot construct it after it loads.

```ts
@Component({
  selector: 'app-report',
  template: `<button (click)="export()">Export</button>`,
})
export class Report {
  private exporter = injectAsync(() => import('./report-exporter').then((m) => m.ReportExporter));

  async export() {
    const exporter = await this.exporter();
    exporter.export();
  }
}
```

The first call to `this.exporter()` triggers the dynamic import; later calls reuse the same promise, so the chunk is fetched once.

For a default export, pass the dynamic import directly and Angular unwraps `default`:

```ts
private exporter = injectAsync(() => import('./report-exporter'));
```

Prefetch: by default the chunk is fetched only when you invoke the returned function. Pass a `prefetch` trigger (any function returning a `Promise`) to start earlier. `onIdle` waits until the browser is idle:

```ts
injectAsync(() => import('./report-exporter').then((m) => m.ReportExporter), {prefetch: onIdle});
injectAsync(loader, {prefetch: () => onIdle({timeout: 1_000})});
```

Prefetching is opportunistic: if the user invokes the feature first, Angular loads immediately and resolves your `await` when ready.

Custom trigger (a `PrefetchTrigger`; the loader runs when the promise resolves):

```ts
export function onHover(target: HTMLElement): PrefetchTrigger {
  return () =>
    new Promise<void>((resolve) => {
      target.addEventListener('pointerenter', () => resolve(), {once: true});
    });
}
```

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/di/lazy-loading-services (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
