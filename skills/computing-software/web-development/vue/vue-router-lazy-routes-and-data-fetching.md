---
id: computing-software.web-development.vue.vue-router-lazy-routes-and-data-fetching
name: vue-router-lazy-routes-and-data-fetching
category: computing-software
field: web-development
product: vue
tags: [vue, lazy-routes, vue-router, code-splitting, data-fetching, navigation-guards, data-loaders, web-development]
level: practitioner
status: verified
description: "Lazy-loading Vue Router routes and fetching data on navigation: dynamic imports, chunk naming, fetch-before vs after navigation, guards, loaders and errors."
sources:
  - https://router.vuejs.org/guide/advanced/lazy-loading.html
  - https://router.vuejs.org/guide/advanced/data-fetching.html
  - https://router.vuejs.org/guide/advanced/navigation-guards.html
  - https://uvr.esm.is/data-loaders/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy-loaded routes and data fetching on navigation

**Goal:** small initial bundles, and route data that loads predictably with loading and error states.

## 1. Lazy routes
```ts
const routes = [
  { path: "/", component: () => import("./views/Home.vue") },
  { path: "/admin", component: () => import("./views/Admin.vue"), meta: { requiresAuth: true } },
];
```
Each dynamic import becomes a chunk loaded on first navigation. Don't use `defineAsyncComponent` for route components. To get fewer, larger chunks, configure chunking in the Vite build options (in Vite 8 `build.rollupOptions` is a deprecated alias of `build.rolldownOptions`; check the chunking option name in the Vite/Rolldown docs for your version).

## 2. Two data-fetching strategies
**Fetch after navigation** (show page skeleton immediately):
```ts
const route = useRoute();
const post = ref(null), error = ref(null), loading = ref(false);
watch(() => route.params.id, async (id) => {
  loading.value = true; error.value = null;
  try { post.value = await getPost(id as string); } catch (e) { error.value = e; } finally { loading.value = false; }
}, { immediate: true });
```
Watching the param matters: navigating `/posts/1` -> `/posts/2` reuses the component.

**Fetch before navigation** (old page stays until data is ready):
```ts
router.beforeResolve(async (to) => {
  if (to.meta.load) {
    try { to.meta.data = await to.meta.load(to); }
    catch { return { name: "error" }; }    // or return false to cancel
  }
});
```
Or in-component `beforeRouteEnter` (call `next` when the fetch completes) / `beforeRouteUpdate` (router docs). Show a global progress bar during pending navigation.

## 3. Data loaders
The router docs have a "Data Loaders" section (Basic Loader, Colada Loader). `unplugin-vue-router` data loaders (`defineBasicLoader`, `defineColadaLoader`) are composables called in a page's `setup` (exported so other components can reuse them), awaited in a navigation guard, and return `{ data, isLoading, error, reload }`. Nuxt users: `useFetch`/`useAsyncData` handle this.

## 4. Chunk load failures
After a deploy old chunks 404. Handle:
```ts
// Vite emits `vite:preloadError` when a dynamic import fails to load (Vite build guide)
window.addEventListener("vite:preloadError", (event) => {
  event.preventDefault();        // the error is not thrown
  window.location.reload();      // or navigate to the target route with a full page load
});
// Without Vite, match the browser-specific error message in router.onError (wording differs per browser).
```

## 5. Guards
Use `meta` + a global `beforeEach` for auth redirects (`return { name: "login", query: { redirect: to.fullPath } }`). Return values rather than using the `next()` callback (still supported, but the router docs discourage it).

## Verify
- [ ] Network tab: admin chunk loads only when visiting /admin.
- [ ] Switching between `/posts/1` and `/posts/2` refetches.
- [ ] Simulated chunk 404 recovers with a reload rather than a blank page.
