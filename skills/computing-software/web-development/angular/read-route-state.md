---
id: computing-software.web-development.angular.read-route-state
name: read-route-state
category: computing-software
field: web-development
product: angular
tags: [angular, routing, activatedroute, snapshot, query-params, matrix-params, routerlinkactive, isactive]
level: practitioner
status: docs-checked
description: "Read Angular route state: ActivatedRoute properties, snapshots, route, query and matrix params, RouterLinkActive with exact matching, and the isActive signal."
sources:
  - https://angular.dev/guide/routing/read-route-state
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ActivatedRoute` (inject it) exposes: `url` (Observable of `UrlSegment[]`), `data` (route data plus resolved values), `params`, `queryParams`, and `resources` (read-only `Resource` instances; requires `withRouterResources()`).

Snapshots are static and do not reflect later changes:

```ts
this.userId = this.route.snapshot.paramMap.get('id');
const snapshot = this.route.snapshot; // snapshot.url, snapshot.params, snapshot.queryParams
```

Route params (`{path: 'product/:id'}`): subscribe, e.g. `this.activatedRoute.params.subscribe((params) => this.productId.set(params['id']));`.

Query params suit filtering, sorting and pagination and can persist across navigation. Set with `router.navigate(['/products'], {queryParams: {category: 'electronics', sort: 'price', page: 1}})`, read with `route.queryParams`. Use `queryParamsHandling: 'merge'` to preserve others:

```ts
this.router.navigate([], {queryParams: {sort}, queryParamsHandling: 'merge'});
```

Matrix params are optional and scoped to one path segment, with semicolons, needing no route config: `this.router.navigate(['/awesome-products', {view: 'grid', filter: 'new'}])` gives `/awesome-products;view=grid;filter=new`. Read them from `route.params`; they are also bound to component inputs with `withComponentInputBinding`.

Active styling: `<a routerLink="/about" routerLinkActive="active-button" ariaCurrentWhenActive="page">`. Multiple classes: `routerLinkActive="class1 class2"` or `[routerLinkActive]="['class1', 'class2']"`. `routerLinkActive` alone does not set `aria-current`; set `ariaCurrentWhenActive` so users who cannot perceive the styling can identify the active link.

Matching: by default ancestors count, so visiting `/user/jane/role/admin` activates links to both `/user/jane` and `/user/jane/role/admin`. Use `[routerLinkActiveOptions]="{exact: true}"` for exact matches; this is sugar for `{paths: 'exact', fragment: 'ignored', matrixParams: 'ignored', queryParams: 'exact'}` (`exact: false` is `paths: 'subset'` and `queryParams: 'subset'`). `routerLinkActive` can sit on an ancestor element wrapping several links.

`isActive` returns a computed signal:

```ts
isSettingsActive = isActive('/settings', this.router, {
  paths: 'subset', queryParams: 'ignored', fragment: 'ignored', matrixParams: 'ignored',
});
```

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/routing/read-route-state (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
