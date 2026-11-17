---
id: computing-software.web-development.angular.defer-practices-testing
name: defer-practices-testing
category: computing-software
field: web-development
product: angular
tags: [angular, defer, testing, deferblockbehavior, ssr, hmr, barrel-files, accessibility, cls]
level: advanced
status: docs-checked
description: "Test @defer blocks with DeferBlockBehavior.Manual, plus SSR, HMR and barrel-file caveats and best practices for layout shift and accessibility."
sources:
  - https://angular.dev/guide/templates/defer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Testing: TestBed plays defer blocks through like the real app by default. To step through states manually set `deferBlockBehavior` to `Manual`:

```ts
TestBed.configureTestingModule({deferBlockBehavior: DeferBlockBehavior.Manual});
const componentFixture = TestBed.createComponent(ExampleA);
const deferBlockFixture = (await componentFixture.getDeferBlocks())[0];
expect(componentFixture.nativeElement.innerHTML).toContain('Placeholder');
await deferBlockFixture.render(DeferBlockState.Loading);
expect(componentFixture.nativeElement.innerHTML).toContain('Loading');
await deferBlockFixture.render(DeferBlockState.Complete);
```

Caveats:
- HMR: while Hot Module Replacement is active, all `@defer` chunks are fetched eagerly, overriding triggers. Serve with `--no-hmr` to restore normal trigger behavior.
- SSR and SSG: by default defer blocks render their `@placeholder` (or nothing) on the server and triggers are not invoked; on the client the placeholder is hydrated and triggers are activated. To render main content on the server, enable Incremental Hydration and configure `hydrate` triggers.
- Barrel files: importing a deferred component through a barrel (`index.ts`) keeps all its exports in one module, so the component stays in the main bundle. Import directly from the component file (`import {HeavyComponent} from './heavy.component';`) so the bundler can split a lazy chunk.

Best practices:
- Nested `@defer` blocks should have different triggers, otherwise they load simultaneously, causing cascading requests that may hurt page load.
- Avoid deferring components visible in the initial viewport, which can raise cumulative layout shift. If necessary, avoid `immediate`, `timer`, `viewport` and custom `when` triggers that load during the initial render.
- Screen readers read the placeholder or loading content but may not announce when deferred content loads. Wrap the block in a live region:

```html
<div aria-live="polite" aria-atomic="true">
  @defer (on timer(2000)) {
    <user-profile [user]="currentUser" />
  } @placeholder {
    Loading user profile...
  } @loading {
    Please wait...
  } @error {
    Failed to load profile
  }
</div>
```

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/templates/defer (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
