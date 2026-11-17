---
id: computing-software.web-development.vue.vue-router-and-pinia-state-management
name: vue-router-and-pinia-state-management
category: computing-software
field: web-development
product: vue
tags: [vue, vue-router, pinia, navigation-guards, state-management, composables, vuex, web-development]
level: advanced
status: verified
description: "Vue Router navigation guards (and their async/redirect gotchas) and Pinia store patterns for state shared across components."
sources:
  - https://router.vuejs.org/guide/advanced/navigation-guards.html
  - https://pinia.vuejs.org/core-concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vue Router guards and Pinia stores

**Goal:** gate navigation correctly (auth, unsaved-changes prompts) and share
state across components without the boilerplate Vuex required.

## 1. Navigation guard order and what each is for
- **Global `beforeEach`** (on the router): runs for every navigation — the right
  place for auth checks (`if (!store.user) return '/login'`).
- **Per-route `beforeEnter`**: only for that route; use for a check specific to
  one page rather than duplicating logic in the global guard with a path check.
- **In-component `beforeRouteLeave`** (Composition API: `onBeforeRouteLeave`): runs in the component being left, so it can read the component's own dirty-state — the right place for
  "you have unsaved changes, leave anyway?".
Full order (router docs): `beforeRouteLeave` → global `beforeEach` → `beforeRouteUpdate` → route `beforeEnter` → async route components resolved → `beforeRouteEnter` → global `beforeResolve` → navigation confirmed → `afterEach`. Know this before assuming a check in one will or won't have
run by the time another executes.

## 2. The async guard gotcha
```js
router.beforeEach(async (to) => {
  const ok = await checkAuth();     // navigation pauses until this resolves
  if (!ok) return '/login';
});
```
A guard returns a value to redirect/cancel — returning `false` cancels, returning a path
string/object redirects, returning nothing/`true` proceeds. Throwing an error also cancels the navigation and calls `router.onError()` handlers. `next()` is still supported but is a common source of mistakes; prefer return values. Forgetting to
`return` the redirect value (calling `router.push('/login')` inside the guard
*instead of* returning it) can race with the in-progress navigation and
produce duplicate-navigation warnings or a flash of the guarded page.

## 3. Pinia basics that replace most Vuex boilerplate
```js
export const useCartStore = defineStore('cart', {
  state: () => ({ items: [] }),
  getters: { total: (state) => state.items.reduce((s, i) => s + i.price, 0) },
  actions: {
    add(item) { this.items.push(item); },               // direct mutation, no separate mutations file
    async checkout() { await api.post('/checkout', this.items); this.items = []; },
  },
});
```
No separate mutations layer (actions can mutate `this` directly) and no
manual module namespacing — each `defineStore` call is its own isolated store,
imported wherever needed via its composable (`useCartStore()`). This is the
main simplification over Vuex: less ceremony for the same capability.

## 4. Store composition — splitting stores vs. one big store
Prefer several focused stores (`useAuthStore`, `useCartStore`, `useUiStore`)
over one store with everything — a component depending on `useCartStore()`
alone doesn't re-run/re-subscribe on unrelated auth state changes, and the
store file stays navigable. A store can use another store inside an action
(`const auth = useAuthStore()`) for cross-store coordination.

## 5. Reactivity gotchas carried over from Vue's reactivity system
Destructuring reactive state out of a Pinia store loses reactivity exactly like
destructuring a `reactive()` object does — `const { items } = useCartStore()`
gives a static snapshot, not a live binding. Use `storeToRefs`:
```js
const { items, total } = storeToRefs(useCartStore());  // each becomes a reactive ref
```
Actions can be destructured directly (`const { add } = useCartStore()`) since
functions don't need the same ref-wrapping — only state/getters need
`storeToRefs`.

## 6. Testing stores and guards
Pinia stores are plain objects in tests — `setActivePinia(createPinia())` in a
`beforeEach`, then call the store directly with no component needed. Test
navigation guards by calling the guard function directly with mock `to`/`from`
objects rather than mounting a full router for logic-only coverage.

## Verify
- [ ] Auth/role checks live in a global `beforeEach`, not duplicated per route.
- [ ] Unsaved-changes prompts use `beforeRouteLeave` in the component, not a global guard.
- [ ] Every async guard explicitly `return`s its redirect/cancel value.
- [ ] State/getters pulled from a Pinia store for template binding go through `storeToRefs`.
- [ ] Stores are split by concern rather than one store holding unrelated domains.
