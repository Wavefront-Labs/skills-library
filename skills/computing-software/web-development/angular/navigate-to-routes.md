---
id: computing-software.web-development.angular.navigate-to-routes
name: navigate-to-routes
category: computing-software
field: web-development
product: angular
tags: [angular, routing, routerlink, router-navigate, navigatebyurl, relativeto, browserurl, scroll]
level: practitioner
status: docs-checked
description: "Navigate in Angular with RouterLink and Router: relative versus absolute links, navigate and relativeTo, navigateByUrl, replaceUrl, browserUrl and scroll manual."
sources:
  - https://angular.dev/guide/routing/navigate-to-routes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Declarative: import `RouterLink` and use `<a routerLink="/settings">`. Strings are the common form; use the array form for dynamic segments: `<a [routerLink]="['user', currentUserId]">`. A leading `/` is relative to the root; without it, relative to the current URL. On `example.com/settings`, `routerLink="notifications"` and `routerLink="/settings/notifications"` both go to `/settings/notifications`. Relative URLs are preferred as more maintainable.

Programmatic: inject `Router`.

```ts
this.router.navigate(['/users', userId]);
this.router.navigate(['/search'], {queryParams: {category: 'books', sort: 'price'}});
this.router.navigate(['/products', {featured: true, onSale: true}]); // matrix params
```

`relativeTo` with `ActivatedRoute`:

```ts
this.router.navigate(['edit'], {relativeTo: this.route});        // /users/123 -> /users/123/edit
this.router.navigate(['..'], {relativeTo: this.route});          // -> /users
this.router.navigate(['..', 'list'], {relativeTo: this.route});  // -> /users/list
```

When going up several levels, all `..` segments must be in the first element: `['../../settings']` (from `/team/123/users/456` to `/team/123/settings`). Only the first command string is parsed for `..`. Never prefix the first command with `/` when using `relativeTo`: a leading `/` makes navigation absolute and ignores `relativeTo` (`['/edit']` gives `/edit`).

`navigateByUrl` takes a URL string, suited to absolute navigation, external URLs and deep links:

```ts
router.navigateByUrl('/products/123?view=details#reviews');
router.navigateByUrl('/checkout', {replaceUrl: true}); // replace current history entry
```

Different address bar URL: `router.navigateByUrl('/not-found', {browserUrl: '/products/missing-item'})` renders `/not-found` but shows `/products/missing-item`; it only affects the address bar. `RouterLink` has a `browserUrl` input too: `<a [routerLink]="['/dashboard']" [browserUrl]="'/home'">`, which also accepts a `UrlTree` from `router.createUrlTree(...)`.

Scrolling: with `withInMemoryScrolling({scrollPositionRestoration: 'enabled'})` (or `'top'`) the router scrolls to top after a link click, even for query-only changes. Opt out per link with `scroll="manual"` (default `'after-transition'`), or programmatically `router.navigateByUrl('/products/42?tab=reviews', {scroll: 'manual'})`.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/routing/navigate-to-routes (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
