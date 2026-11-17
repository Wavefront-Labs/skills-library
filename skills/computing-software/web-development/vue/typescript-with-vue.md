---
id: computing-software.web-development.vue.typescript-with-vue
name: typescript-with-vue
category: computing-software
field: web-development
product: vue
tags: [vue, vue-typescript, vue-tsc, typed-props, defineprops, generic-components, volar, web-development]
level: practitioner
status: verified
description: "Using TypeScript with Vue 3: vue-tsc type checking, type-based defineProps/defineEmits, defaults, typed refs and provide/inject, generic components and Vue Language Tools."
sources:
  - https://vuejs.org/guide/typescript/overview.html
  - https://vuejs.org/guide/typescript/composition-api.html
  - https://github.com/vuejs/language-tools
  - https://vuejs.org/api/sfc-script-setup.html#generics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TypeScript with Vue

**Goal:** type-checked templates and components in editor and CI.

## 1. Tooling
- Editor: Vue - Official extension (Vue Language Tools, formerly Volar). Disable Vetur.
- CI: `vue-tsc --noEmit` (tsc can't read `.vue` files). `create-vue` adds a `type-check` script (`vue-tsc --build`) and `tsconfig.app.json` with `@vue/tsconfig`. vue-tsc needs TypeScript 5.x (checked with 5.x; vue-tsc 3.3.13 was not run against TypeScript 7).
- Vite only strips types; it doesn't type-check builds - run `vue-tsc` separately.

## 2. Props and emits
```vue
<script setup lang="ts">
interface Props { title: string; size?: "sm" | "md"; items?: string[] }
const { title, size = "md", items = [] } = defineProps<Props>();   // 3.5+ reactive destructure defaults (write the array literal; `items = () => []` fails to compile: "Default value of prop does not match declared type")
const emit = defineEmits<{ select: [id: string]; close: [] }>();
const model = defineModel<string>({ required: true });
</script>
```
Before 3.5 use `withDefaults(defineProps<Props>(), { size: "md", items: () => [] })`. Object/array defaults must be factories.

## 3. Refs and computed
```ts
const user = ref<User | null>(null);
const count = ref(0);                       // inferred
const total = computed<number>(() => items.value.length);
const el = useTemplateRef<HTMLInputElement>("input");
```

## 4. provide/inject
```ts
export const ThemeKey: InjectionKey<Ref<"light" | "dark">> = Symbol("theme");
provide(ThemeKey, theme);
const theme = inject(ThemeKey);             // Ref<...> | undefined
```

## 5. Generic components
```vue
<script setup lang="ts" generic="T extends { id: string }">
defineProps<{ items: T[]; selected?: T }>();
defineEmits<{ pick: [item: T] }>();
</script>
```

## 6. Events and template expressions
Type DOM events in handlers: `(e: Event) => (e.target as HTMLInputElement).value`. Templates are type-checked by vue-tsc - including props passed to child components and slot props (`defineSlots<{ default(props: { item: T }): any }>()`).

## 7. Global augmentation
Router meta: `declare module "vue-router" { interface RouteMeta { requiresAuth?: boolean } }`. Global components: `declare module "vue" { interface GlobalComponents { RouterLink: typeof RouterLink } }`.

## Verify
- [ ] `vue-tsc --noEmit` passes in CI.
- [ ] Passing a wrong prop type in a template fails type check (try once).
- [ ] No `any` props; emits are typed.
