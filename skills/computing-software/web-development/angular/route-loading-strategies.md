---
id: computing-software.web-development.angular.route-loading-strategies
name: route-loading-strategies
category: computing-software
field: web-development
product: angular
tags: [angular, routing, lazy-loading, loadcomponent, loadchildren, eager, code-splitting]
level: practitioner
status: docs-checked
description: "Angular route loading: eager component routes versus lazy loadComponent and loadChildren, default exports, and inject() inside loaders."
sources:
  - https://angular.dev/guide/routing/loading-strategies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Eager: a route using the `component` property is bundled with the route configuration file. The browser downloads and parses it on initial load (slower initial load) but it is available immediately, which can make transitions more seamless.

```ts
{path: '', component: HomePage},
{path: 'login', component: LoginPage},
```

Lazy: `loadComponent` lazily loads a component when the route becomes active; `loadChildren` lazily loads child routes during route matching.

```ts
{path: 'login', loadComponent: () => import('./components/auth/login-page')},
{
  path: 'admin',
  loadComponent: () => import('./admin/admin.component'),
  loadChildren: () => import('./admin/admin.routes'),
},
```

Both accept a loader returning a Promise of a component or a set of routes, normally via dynamic `import()`, though any async loader works. If the file uses a `default` export, return the `import()` promise directly without `.then`. Code compiles into separate chunks the router requests only when the user visits the route.

Injection context: the router runs `loadComponent` and `loadChildren` in the injection context of the current route, so `inject()` can reach providers on that route, inherited from parents, or global:

```ts
loadComponent: () => {
  const flags = inject(FeatureFlags);
  return flags.isPremium ? import('./dashboard/premium-dashboard') : import('./dashboard/basic-dashboard');
},
```

Choosing: eager loading is generally recommended for primary landing pages, lazy for other pages. Lazy routes reduce initial data but add future requests; nested lazy loading across several levels can significantly impact performance.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/routing/loading-strategies (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
