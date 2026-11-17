---
id: computing-software.web-development.angular.define-routes
name: define-routes
category: computing-software
field: web-development
product: angular
tags: [angular, routing, routes, providerouter, wildcard, route-params, titlestrategy, children]
level: intro
status: docs-checked
description: "Define Angular routes: path params, wildcards, first-match ordering, redirects, titles and TitleStrategy, route providers, static data and child routes."
sources:
  - https://angular.dev/guide/routing/define-routes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A route is an object saying which component renders for a URL path. Keep them in a `routes` file (CLI projects use `src/app/app.routes.ts`) and register with `provideRouter(routes)` in the `providers` of `ApplicationConfig`.

```ts
export const routes: Routes = [
  {path: '', component: HomePage},
  {path: 'admin', component: AdminPage},
];
```

Parameters: prefix with a colon, e.g. `{path: 'user/:id', component: UserProfile}`, or several: `user/:id/:social-media`. Names must start with a letter and may contain letters, numbers, underscore and hyphen. Route params are distinct from the query string.

Wildcard: `{path: '**', component: NotFound}`, typically placed last.

Matching is first-match wins, so put specific routes before less specific ones:

```ts
const routes: Routes = [
  {path: '', component: Home},
  {path: 'users/new', component: NewUser},   // static, most specific
  {path: 'users/:id', component: UserDetail}, // dynamic
  {path: 'users', component: Users},
  {path: '**', component: NotFound},          // always last
];
```

Redirect: `{path: 'articles', redirectTo: '/blog'}` sends users with outdated links to an alternative route.

Titles: `title: 'Home Page'` updates the page title on activation; titles are necessary for an accessible experience. `title` can be a `ResolveFn` (`(route) => route.queryParams['id']`). For central control, extend `TitleStrategy`, implement `updateTitle(snapshot)` (using `this.buildTitle(snapshot)` and `Title.setTitle`) and provide `{provide: TitleStrategy, useClass: AppTitleStrategy}`. The default is `DefaultTitleStrategy`.

Route providers: `providers: [AdminService, {provide: ADMIN_API_KEY, useValue: '12345'}]` on a route gives those dependencies only to that route's content.

Static data: `data: {analyticsId: '456'}`, read by injecting `ActivatedRoute`. For dynamic data use resources or resolvers.

Child routes: `children: [{path: 'info', component: ProductInfo}, {path: 'reviews', component: ProductReviews}]`. The parent component includes its own `<router-outlet />`, and navigation among children updates only the nested outlet.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/routing/define-routes (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
