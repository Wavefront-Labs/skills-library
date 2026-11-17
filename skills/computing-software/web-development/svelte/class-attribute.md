---
id: computing-software.web-development.svelte.class-attribute
name: class-attribute
category: computing-software
field: web-development
product: svelte
tags: [class-attribute, clsx-classes, class-directive, class-value-type, conditional-classes]
level: practitioner
status: docs-checked
description: "Set classes in Svelte: attribute with object or array values via clsx (5.16+), merging local and prop classes, ClassValue type (5.19+), and the older class: directive."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/18-class.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Primitive values act like any attribute: `class={large ? 'large' : 'small'}`. For historical reasons falsy values such as `false` and `NaN` are stringified (`class="false"`), while `undefined` or `null` omit the attribute; a future version will omit for all falsy values.

Since 5.16, `class` can be an object or array, converted with clsx. Objects add truthy keys; arrays combine truthy values:

```svelte
<div class={{ cool, lame: !cool }}>...</div>
<div class={[faded && 'saturate-0 opacity-50', large && 'scale-200']}>...</div>
```

One condition can set several classes (handy with Tailwind). Arrays may contain arrays and objects, which clsx flattens, so a component can combine local classes with a prop:

```svelte
<button {...props} class={['cool-button', props.class]}>
  {@render props.children?.()}
</button>
```

Callers can then pass `class={{ 'bg-blue-700 sm:w-1/2': useTailwind }}`.

Since 5.19, `ClassValue` from `svelte/elements` types a class prop: `const props: { class: ClassValue } = $props();`.

The `class:` directive (before 5.16) is equivalent: `class:cool={cool} class:lame={!cool}`, with shorthand `class:cool`. Unless you use an older version, prefer the attribute, which is more powerful and composable.

## Checked

2026-11-08. Read the class page in full. All claims matched; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
