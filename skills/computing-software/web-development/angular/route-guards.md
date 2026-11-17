---
id: computing-software.web-development.angular.route-guards
name: route-guards
category: computing-software
field: web-development
product: angular
tags: [angular, routing, guards, canactivate, canactivatechild, candeactivate, canmatch, urltree]
level: practitioner
status: docs-checked
description: "Angular route guards: CanActivate, CanActivateChild, CanDeactivate and CanMatch functions, return types, redirects with UrlTree, ordering and server-side checks."
sources:
  - https://angular.dev/guide/routing/route-guards
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Never rely on client-side guards as the sole access control: JavaScript in a browser can be modified. Always enforce authorization server-side too.

Generate with `ng generate guard CUSTOM_NAME` (file `CUSTOM_NAME-guard.ts`). Guards have access to services provided at the route level.

Return types, shared by all guards:
- `boolean`: `true` allows, `false` blocks (except `CanMatch`).
- `UrlTree` or `RedirectCommand`: redirect instead of blocking. To redirect, return one of these; do not return `false` and then call `navigate`.
- `Promise<T>` or `Observable<T>`: the router uses the first emitted value and unsubscribes.

Types:
- `CanActivate` (`route: ActivatedRouteSnapshot`, `state: RouterStateSnapshot`): access to a route, e.g. authentication.

```ts
export const authGuard: CanActivateFn = (route, state) => inject(AuthService).isAuthenticated();
```

- `CanActivateChild` (`childRoute`, `state`): protects child routes; it runs for all children, once per nested child.
- `CanDeactivate` (`component`, `currentRoute`, `currentState`, `nextState`): leaving a route, e.g. unsaved forms.

```ts
export const unsavedChangesGuard: CanDeactivateFn<Form> = (component) =>
  component.hasUnsavedChanges() ? confirm('You have unsaved changes. Are you sure you want to leave?') : true;
```

- `CanMatch` (`route: Route`, `segments: UrlSegment[]`, `currentSnapshot: PartialMatchRouteSnapshot`): whether a route can match during path matching. When it returns `false`, the router tries other matching routes rather than blocking, useful for feature flags, A/B tests, or different components for the same path:

```ts
{path: 'dashboard', component: AdminDashboard, canMatch: [adminGuard]},
{path: 'dashboard', component: UserDashboard, canMatch: [userGuard]},
```

Apply them as arrays on the route: `canActivate: [authGuard, adminGuard]`, `canDeactivate: [...]`, `canActivateChild: [authGuard]` (with `children`), `canMatch: [featureToggleGuard]`.

Order: the router starts guards in array order but does not wait for one to finish before starting the next, so Promise or Observable guards run concurrently. Navigation continues only if every guard returns `true`; otherwise the result of the first guard in the array that did not return `true` is used, even if a later guard finished earlier. A guard must not rely on work done by an earlier guard in the same array (such as loading the user); put it in a shared service or combine the checks into one guard.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/routing/route-guards (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
