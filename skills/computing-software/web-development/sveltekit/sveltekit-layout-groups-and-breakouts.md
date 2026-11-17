---
id: computing-software.web-development.sveltekit.sveltekit-layout-groups-and-breakouts
name: sveltekit-layout-groups-and-breakouts
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, layout-groups, route-groups, layouts, layout-reset, routing, advanced-layouts]
level: practitioner
status: docs-checked
description: "Share or reset SvelteKit layouts with (group) directories and +page@ / +layout@ breakouts, and know when composition is simpler."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/10-advanced-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make the layout hierarchy differ from the route hierarchy.

## (group)
A directory wrapped in parentheses groups routes under a layout without changing the URL:
```tree
src/routes/
│ (app)/
│ ├ dashboard/
│ ├ item/
│ └ +layout.svelte
│ (marketing)/
│ ├ about/
│ ├ testimonials/
│ └ +layout.svelte
├ admin/
└ +layout.svelte
```
A `+page` can sit directly in a group (e.g. `/` as an app or marketing page). `/admin` here inherits neither group layout. The root layout defaults to `{@render children()}` if omitted; to exclude routes from common layouts, put everything else inside groups.

## +page@
Append `@` plus a segment name (empty for root) to reset to that ancestor layout. For `(app)/item/[id]/embed/+page.svelte`:
- `+page@[id].svelte` inherits `(app)/item/[id]/+layout.svelte`
- `+page@item.svelte` inherits `(app)/item/+layout.svelte`
- `+page@(app).svelte` inherits `(app)/+layout.svelte`
- `+page@.svelte` inherits `src/routes/+layout.svelte`

## +layout@
Layouts can reset the same way: `+layout@.svelte` resets for all child routes. Example comments:
```
│ │ ├ +layout@.svelte   // inherits from root layout, skipping (app)/+layout.svelte
```

## When not to use groups
If groups would nest awkwardly or serve one outlier, use composition (reusable `load` functions or Svelte components) or if-statements:
```svelte
<!--- file: src/routes/nested/route/+layout@.svelte --->
<script>
	import ReusableLayout from '#lib/ReusableLayout.svelte';
	let { data, children } = $props();
</script>

<ReusableLayout {data}>
	{@render children()}
</ReusableLayout>
```
```js
/// file: src/routes/nested/route/+layout.js
import { reusableLoad } from '#lib/reusable-load-function.js';

export function load(event) {
	// Add additional logic here, if needed
	return reusableLoad(event);
}
```

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `30-advanced/10-advanced-routing.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
