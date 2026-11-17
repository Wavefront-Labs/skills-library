---
id: computing-software.web-development.vue.writing-composables
name: writing-composables
category: computing-software
field: web-development
product: vue
tags: [vue, composables, vueuse, composable-patterns, composition-api, maybe-ref, tovalue, web-development]
level: practitioner
status: verified
description: "Writing Vue composables like VueUse: naming, accepting refs or getters with toValue, returning refs, cleanup with onScopeDispose, SSR safety and async patterns."
sources:
  - https://vuejs.org/guide/reusability/composables.html
  - https://vueuse.org/guide/best-practice.html
  - https://vuejs.org/api/reactivity-utilities.html#tovalue
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing composables

**Goal:** reusable stateful logic that accepts reactive inputs, returns reactive outputs and cleans up after itself.

## 1. Shape
```ts
// useFetch.ts
import { ref, watchEffect, toValue, type MaybeRefOrGetter } from "vue";

export function useFetch<T>(url: MaybeRefOrGetter<string>) {
  const data = ref<T | null>(null);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  watchEffect(async (onCleanup) => {
    const ctrl = new AbortController();
    onCleanup(() => ctrl.abort());
    loading.value = true; error.value = null;
    try {
      const res = await fetch(toValue(url), { signal: ctrl.signal });   // toValue read before await => tracked
      data.value = await res.json();
    } catch (e) { if ((e as Error).name !== "AbortError") error.value = e as Error; }
    finally { loading.value = false; }
  });
  return { data, error, loading };
}
```
Usage: `const { data } = useFetch(() => `/api/users/${id.value}`)`.

## 2. Conventions
- Name `useXxx`; call only synchronously in `setup` (or another composable).
- Accept `MaybeRefOrGetter` inputs, normalise with `toValue()` inside a watcher/computed so changes are tracked.
- Return a plain object of refs (not `reactive`) so callers can destructure without losing reactivity.
- Register cleanup with `onScopeDispose` (works inside components and `effectScope`), or `onUnmounted` when DOM-related.

## 3. Shared state
State declared inside the function is per call. Module-level state is a global singleton - fine for client-only apps, but on SSR it's shared across requests. Use Pinia or `provide/inject` for shared state, or VueUse `createGlobalState`/`createSharedComposable` (client).

## 4. SSR safety
Touch `window`/`document` only in `onMounted` or guarded by `typeof window !== "undefined"`. Check the docs of each VueUse function for its SSR behaviour.

## 5. Reach for VueUse first
`useEventListener`, `useIntersectionObserver`, `useDebounceFn`, `useLocalStorage`, `useMediaQuery`, `useElementSize` - ready-made and (per function) cleaned up automatically. Write your own when logic is domain-specific.

## 6. Async composables
Don't `await` at the top of a composable called in setup unless the component is inside `<Suspense>`; return refs that fill later instead.

## Verify
- [ ] Changing the input ref triggers a refetch; the previous request is aborted.
- [ ] Unmounting the component leaves no listeners/timers (check with a log in cleanup).
- [ ] Unit test the composable with `withSetup` helper or `effectScope` + `nextTick`.
