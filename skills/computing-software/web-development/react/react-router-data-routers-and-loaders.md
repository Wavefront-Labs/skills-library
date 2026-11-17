---
id: computing-software.web-development.react.react-router-data-routers-and-loaders
name: react-router-data-routers-and-loaders
category: computing-software
field: web-development
product: react
tags: [react, react-router, data-router, loaders, actions, createbrowserrouter, nested-routes, web-development, react-ecosystem]
level: practitioner
status: docs-checked
description: "Using React Router data routers: createBrowserRouter, nested routes and outlets, loaders and actions, pending UI, errors, lazy routes and revalidation."
sources:
  - https://reactrouter.com/start/data/installation
  - https://reactrouter.com/start/data/routing
  - https://reactrouter.com/start/data/route-object
  - https://reactrouter.com/start/data/actions
  - https://reactrouter.com/how-to/error-boundary
  - https://reactrouter.com/upgrading/v7
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# React Router data routers and loaders

**Goal:** data loads in parallel with code, before render, with route-level errors and mutations that revalidate automatically.

## 1. Router setup (data mode)
```jsx
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";   // v8 removes the react-router-dom package
const router = createBrowserRouter([
  {
    path: "/", Component: Root, ErrorBoundary: RootError,
    children: [
      { index: true, Component: Home },
      { path: "projects/:id", loader: projectLoader, action: projectAction, Component: Project },
    ],
  },
]);
createRoot(el).render(<RouterProvider router={router} />);
```
Parents render `<Outlet />` for children. React Router also has a framework mode (Vite plugin, SSR); this skill covers data mode.

## 2. Loaders
```jsx
import { data } from "react-router";
export async function projectLoader({ params, request }) {
  const res = await fetch(`/api/projects/${params.id}`, { signal: request.signal });
  if (res.status === 404) throw data("Not found", { status: 404 });
  return res.json();
}
function Project() { const project = useLoaderData(); ... }
```
Matched route loaders run in parallel, so nested routes do not wait on each other and there are no fetch-in-effect waterfalls.

## 3. Actions and forms
```jsx
<Form method="post"><input name="title" /><button>Save</button></Form>
export async function projectAction({ request, params }) {
  const fd = await request.formData();
  const errors = validate(fd);
  if (errors) return { errors };               // return plain data
  await save(params.id, fd);
  return redirect(`/projects/${params.id}`);
}
```
After any action, active loaders revalidate. `useActionData()` reads returned errors; `useFetcher()` for mutations that shouldn't navigate (like buttons, inline edits).

## 4. Pending and optimistic UI
`useNavigation().state` (`idle | loading | submitting`) for global indicators; `fetcher.state` and `fetcher.formData` for per-item optimistic UI.

## 5. Errors
`ErrorBoundary` per route; `useRouteError()` + `isRouteErrorResponse(err)` to show 404 vs 500. Thrown `data(...)` values carry a status code.

## 6. Code splitting
`lazy` returns route properties such as `{ loader, Component }`, so the route module and loader code are fetched together before rendering.

## 7. Control revalidation
`shouldRevalidate` on a route to skip expensive reloads (e.g. only when params change).

## Verify
- [ ] Network tab shows loaders for nested routes in parallel, not sequential.
- [ ] Unknown id renders the route error boundary with a 404 message.
- [ ] Submitting a form updates lists without manual refetching.

## Checked

Checked 2026-10-25 against the React Router documentation repository (react-router 8.5.0 released 2026-10-19, docs for data mode). Confirmed: `createBrowserRouter` from `react-router` and `RouterProvider` from `react-router/dom`; v8 removes the `react-router-dom` package; route objects accept `Component`, `ErrorBoundary`, `loader`, `action`, `shouldRevalidate` and `lazy`; loaders return plain data and `useLoaderData` reads it; matched loaders run in parallel; actions read `request.formData()` and all loaders revalidate afterwards; `useActionData`, `useFetcher` (`fetcher.state`, `fetcher.formData`) and `useNavigation`; thrown `data` with a status, `useRouteError` and `isRouteErrorResponse`. Replaced the v6 `json()` and `new Response` guidance and the dead `upgrading/v6` source.

Method: documentation only; no commands were run.
