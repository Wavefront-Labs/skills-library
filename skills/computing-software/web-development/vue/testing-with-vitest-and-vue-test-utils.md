---
id: computing-software.web-development.vue.testing-with-vitest-and-vue-test-utils
name: testing-with-vitest-and-vue-test-utils
category: computing-software
field: web-development
product: vue
tags: [vue, vue-test-utils, vitest, testing-library-vue, component-testing, pinia-testing, web-development]
level: practitioner
status: verified
description: "Testing Vue 3 components with Vitest and Vue Test Utils: mount options, async updates, emitted events, stubbing router/Pinia, composables and avoiding brittle tests."
sources:
  - https://vuejs.org/guide/scaling-up/testing.html
  - https://test-utils.vuejs.org/guide/
  - https://pinia.vuejs.org/cookbook/testing.html
  - https://vitest.dev/guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing with Vitest and Vue Test Utils

**Goal:** fast tests that check behaviour users see, not component internals.

## 1. Setup
```ts
// vitest.config.ts
import { defineConfig } from "vitest/config";
import vue from "@vitejs/plugin-vue";
export default defineConfig({ plugins: [vue()], test: { environment: "jsdom", globals: true } });
```
`npm i -D vitest @vue/test-utils jsdom` (or `happy-dom`). `create-vue` scaffolds this.

## 2. A component test
```ts
import { mount } from "@vue/test-utils";
import Counter from "./Counter.vue";

test("increments and emits", async () => {
  const wrapper = mount(Counter, { props: { start: 1 } });
  await wrapper.get("button").trigger("click");      // await DOM update
  expect(wrapper.text()).toContain("2");
  expect(wrapper.emitted("change")?.[0]).toEqual([2]);
});
```
- Await `trigger`, `setValue`, `setProps` - DOM updates are async. For promises inside components use `await flushPromises()`.
- `get` throws if missing (clear errors); `find` returns an empty wrapper.
- Select by role/text or `data-test` attributes, not CSS classes.

## 3. Global plugins and stubs
```ts
import { createTestingPinia } from "@pinia/testing";
mount(Cart, {
  global: {
    plugins: [createTestingPinia({ createSpy: vi.fn, initialState: { cart: { items: [] } } })],
    stubs: { RouterLink: RouterLinkStub, Teleport: true },
    mocks: { $t: (k: string) => k },
  },
});
```
Router: use a real `createRouter({ history: createMemoryHistory(), routes })`, `router.push()` then `await router.isReady()` - more reliable than mocking `useRoute`.

## 4. Slots and v-model
```ts
mount(Card, { slots: { default: "<p>Body</p>", header: "<h2>Title</h2>" } });
const w = mount(Input, { props: { modelValue: "", "onUpdate:modelValue": (v) => w.setProps({ modelValue: v }) } });
```

## 5. Composables
Test pure composables directly; ones using lifecycle hooks/inject need a host component (`withSetup` helper that mounts a component calling the composable).

## 6. Testing Library alternative
`@testing-library/vue` (`render`, `screen.getByRole`, `userEvent`) for user-centric tests; works alongside VTU.

## 7. E2E
Component tests don't cover routing/SSR/network. Use Playwright or Cypress for critical flows; Vitest browser mode for real-browser component tests.

## Verify
- [ ] `vitest run --coverage` in CI.
- [ ] Tests survive refactors of internal state (no `wrapper.vm` poking).
- [ ] No unawaited triggers (review async tests carefully).
