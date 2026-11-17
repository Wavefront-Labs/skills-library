---
id: computing-software.web-development.svelte.what-are-runes
name: what-are-runes
category: computing-software
field: web-development
product: svelte
tags: [runes, rune-keywords, svelte-5, dollar-prefix, svelte-compiler-symbols]
level: intro
status: docs-checked
description: "What Svelte 5 runes are: dollar-prefixed compiler keywords valid in .svelte and .svelte.js/.svelte.ts files, needing no import, and differing from ordinary functions."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/01-what-are-runes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Runes are symbols you use in `.svelte` and `.svelte.js`/`.svelte.ts` files to control the Svelte compiler. Think of them as keywords of the Svelte language. They have a `$` prefix and look like functions:

```js
let message = $state('hello');
```

How they differ from normal functions:
- No import needed; they are part of the language.
- They are not values: you cannot assign one to a variable or pass it as an argument.
- Like JavaScript keywords, they are only valid in certain positions; the compiler reports misplaced ones.

Runes did not exist before Svelte 5.

Check: if you want reactive code in a plain module, name the file with `.svelte.js` or `.svelte.ts` so the compiler processes it.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte runes overview page: `$` prefix, usable in .svelte and .svelte.js/.svelte.ts files, no import, not values, position rules, Svelte 5 only. Nothing removed. The closing tip about .svelte.js naming is an inference from the stated file types.
