---
id: computing-software.web-development.angular.router-outlets
name: router-outlets
category: computing-software
field: web-development
product: angular
tags: [angular, routing, router-outlet, named-outlets, child-routes, routeroutletdata]
level: practitioner
status: docs-checked
description: "Render routes with RouterOutlet: placement, nested child outlets, named secondary outlets, outlet lifecycle events and routerOutletData with ROUTER_OUTLET_DATA."
sources:
  - https://angular.dev/guide/routing/show-routes-with-outlets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`RouterOutlet` marks where the router renders the component for the current URL. Import it and place `<router-outlet />` in the template (`imports: [RouterOutlet]`):

```html
<app-header />
<router-outlet />
<app-footer />
```

The `<router-outlet>` stays in the DOM as a reference point; routed content is inserted just after it as a sibling.

Child routes add a second outlet inside the parent route's component, which often has its own `<nav>`. Place child routes in the parent route's `children` array:

```ts
{
  path: 'settings',
  component: Settings, // template contains <router-outlet />
  children: [
    {path: 'profile', component: Profile},
    {path: 'security', component: Security},
  ],
}
```

Named outlets: give each outlet a unique `name` (default `'primary'`): `<router-outlet name="read-more" />`. The name can be bound to a value; when it changes, the outlet destroys its current component and renders the route for the new name if one matches. Match with the route's `outlet` property:

```ts
{path: 'user/:id', component: UserDetails, outlet: 'additional-actions'}
```

Lifecycle events an outlet emits: `activate` (new component instantiated), `deactivate` (component destroyed), `attach` and `detach` (when the `RouteReuseStrategy` attaches or detaches the subtree).

```html
<router-outlet (activate)="onActivate($event)" (deactivate)="onDeactivate($event)"
               (attach)="onAttach($event)" (detach)="onDetach($event)" />
```

Contextual data: bind `routerOutletData` on the outlet and read it as a signal in routed components and their children with the `ROUTER_OUTLET_DATA` token.

```html
<router-outlet [routerOutletData]="{layout: 'sidebar'}" />
```

```ts
outletData = inject(ROUTER_OUTLET_DATA) as Signal<{layout: string}>;
```

When `routerOutletData` is unset, the injected signal's value is `undefined`.

## Checked

Method: 2026-11-08 docs-only read of https://angular.dev/guide/routing/show-routes-with-outlets (the page's raw markdown from the angular/angular repository (adev/src/content/guide), read in full) and compared each claim and example with the skill text. All claims match the page; no changes to the claims.
