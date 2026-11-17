---
id: computing-software.web-development.angular.redirecting-routes
name: redirecting-routes
category: computing-software
field: web-development
product: angular
tags: [angular, routing, redirectto, pathmatch, wildcard, redirectfunction]
level: practitioner
status: docs-checked
description: "Angular route redirects: redirectTo strings with params, pathMatch prefix versus full, the root path trap, and conditional redirectTo functions."
sources:
  - https://angular.dev/guide/routing/redirecting-routes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `redirectTo` on a route to forward users: handy for legacy URLs, default routes, or access control.

```ts
const routes: Routes = [
  {path: 'marketing', redirectTo: 'newsletter'},
  {path: 'legacy-user/:id', redirectTo: 'users/:id'},
  {path: '**', redirectTo: '/login'}, // wildcard redirect
];
```

`pathMatch` controls URL matching:
- `'prefix'` (the default for redirects): only the beginning of the URL needs to match. `{path: 'news', redirectTo: 'blog'}` sends `/news` to `/blog`, `/news/article` to `/blog/article`, and so on.
- `'full'`: the entire URL path must match. `{path: 'news', redirectTo: '/blog', pathMatch: 'full'}` redirects only `/news`; `/news/articles` does not redirect.

Root redirects: `{path: '', redirectTo: '/dashboard', pathMatch: 'full'}` redirects only the root URL. If you do not set `pathMatch: 'full'` on a redirect of the root page (`""`), the router will redirect all URLs.

Conditional: `redirectTo` can be a function returning a string or `UrlTree` (also an observable or promise). It only has access to part of the `ActivatedRouteSnapshot`, since some data (resolved titles, lazy loaded components) is not known during route matching.

```ts
{
  path: 'restaurant/:location/menu',
  pathMatch: 'full',
  redirectTo: (activatedRouteSnapshot) => {
    const location = activatedRouteSnapshot.params['location'];
    const currentHour = new Date().getHours();
    if (activatedRouteSnapshot.queryParams['meal']) {
      return `/restaurant/${location}/menu/${activatedRouteSnapshot.queryParams['meal']}`;
    }
    if (currentHour >= 5 && currentHour < 11) return `/restaurant/${location}/menu/breakfast`;
    if (currentHour >= 11 && currentHour < 17) return `/restaurant/${location}/menu/lunch`;
    return `/restaurant/${location}/menu/dinner`;
  },
},
```

Destination routes are ordinary routes like `{path: 'restaurant/:location/menu/breakfast', component: Menu}`.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/routing/redirecting-routes (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. Claims match the page. The conditional redirect example had dropped the lunch branch; restored it as the page shows it.
