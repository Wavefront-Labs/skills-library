---
id: computing-software.web-development.angular.route-data-resolvers
name: route-data-resolvers
category: computing-software
field: web-development
product: angular
tags: [angular, routing, resolver, resolvefn, withcomponentinputbinding, navigation-error, redirectcommand]
level: practitioner
status: docs-checked
description: "Angular route data resolvers: ResolveFn, resolve config, reading data via ActivatedRoute or input binding, error handling options and parent-child waterfalls."
sources:
  - https://angular.dev/guide/routing/data-resolvers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A resolver is a `ResolveFn` that runs before a route activates and fetches data; the result becomes available through `ActivatedRoute`. It has access to route-level services and receives `ActivatedRouteSnapshot` and `RouterStateSnapshot`. Benefits: no empty states, no spinners for critical data, error handling before navigation, and data consistency which matters for SSR. If you use signals, route resources (non-blocking) are an alternative.

```ts
export const userResolver: ResolveFn<User> = (route, state) => {
  const userStore = inject(UserStore);
  const userId = route.paramMap.get('id')!;
  return userStore.getUser(userId);
};

{path: 'user/:id', component: UserDetail, resolve: {user: userResolver, settings: settingsResolver}}
```

Reading the data:
- `toSignal(this.route.data, {requireSync: true})` then `computed(() => this.data().user as User)`.
- Or add `withComponentInputBinding()` to `provideRouter(routes, ...)` and declare inputs matching the resolver keys: `user = input.required<User>();`.

Error handling: an unhandled resolver failure causes a `NavigationError` and the navigation fails. Three options:
1. Centralise with `withNavigationErrorHandler((error) => { inject(Router).navigate(['/error']); })`; resolvers can then let errors bubble.
2. Subscribe to `router.events` and react to `NavigationError` (custom retry, specific messages, analytics).
3. Handle in the resolver and redirect:

```ts
export const userResolver: ResolveFn<User | RedirectCommand> = (route) => {
  const router = inject(Router);
  return inject(UserStore).getUser(route.paramMap.get('id')!).pipe(
    catchError(() => of(new RedirectCommand(router.parseUrl('/users')))),
  );
};
```

Navigation is blocked while resolvers run. Show feedback with `isNavigating = computed(() => !!this.router.currentNavigation());`.

Best practices from the page: keep resolvers lightweight, handle errors, consider caching, show loading indicators, set reasonable timeouts, use TypeScript types.

Parent to child: resolvers run sequentially from parent to child, and a child resolver can read parent data with `route.parent?.data['user']`. Each nesting level adds to the wait (a network waterfall); route resources run concurrently across routes instead.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/routing/data-resolvers (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
