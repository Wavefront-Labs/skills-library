---
id: computing-software.web-development.vue.template-syntax-and-directives
name: template-syntax-and-directives
category: computing-software
field: web-development
product: vue
tags: [vue-template-syntax, v-bind, v-if, v-for, dynamic-arguments, vue-directives]
level: intro
status: verified
description: "Vue template syntax: interpolation, v-bind and shorthand, same-name shorthand, dynamic arguments, v-if vs v-show, v-for with keys, v-html risks and expression restrictions."
sources:
  - https://vuejs.org/guide/essentials/template-syntax.html
  - https://vuejs.org/guide/essentials/conditional.html
  - https://vuejs.org/guide/essentials/list.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template syntax and directives

## 1. Interpolation and binding
```vue
<p>{{ user.name }} has {{ items.length }} items</p>
<img :src="avatarUrl" :alt="`${user.name}'s avatar`">
<button :disabled="saving" v-bind="buttonAttrs">Save</button>   <!-- object spread -->
<div :id>...</div>                                               <!-- 3.4+: same-name shorthand for :id="id" -->
```
- `{{ }}` escapes HTML; expressions only (no statements, no `if`, no assignments).
- `:attr` is `v-bind:attr`. `null`/`undefined` remove the attribute; boolean attributes follow truthiness.
- Templates can only access a whitelist of globals (`Math`, `Date`...); add others via `app.config.globalProperties`.

## 2. Dynamic arguments
```vue
<a :[attrName]="url">link</a>
<button @[eventName]="handler">Go</button>
```
Argument expressions must evaluate to a string or null; no spaces or quotes inside the brackets; in in-DOM templates names are lowercased.

## 3. Conditionals
```vue
<Spinner v-if="loading" />
<ErrorBox v-else-if="error" :error />
<List v-else :items />
<details v-show="advanced">...</details>
```
- `v-if` creates/destroys (resets component state, runs lifecycle); `v-show` toggles `display` (cheap toggles, always rendered).
- `<template v-if>` groups multiple elements without a wrapper.

## 4. Lists
```vue
<li v-for="item in items" :key="item.id">{{ item.label }}</li>
<li v-for="(value, key, index) in object" :key="key">...</li>
<span v-for="n in 5" :key="n">{{ n }}</span>
```
- Always a stable unique `:key` (not the index if items reorder or are removed).
- Don't put `v-if` and `v-for` on the same element (`v-if` has higher priority in Vue 3); filter in a computed or wrap with `<template v-for>`.

## 5. v-html
`<div v-html="html">` bypasses escaping: only for trusted or sanitised (DOMPurify) content. Scoped styles don't apply inside v-html content.

## 6. Other directives
`v-once` (render once), `v-memo="[a, b]"` (skip re-render unless deps change, for huge lists), `v-pre` (skip compilation), `v-cloak` (hide until mounted, for in-DOM templates).

## Verify
- [ ] No v-if/v-for on the same element; every v-for has a stable key; v-html only on sanitised content (eslint-plugin-vue `vue/no-v-html`).
