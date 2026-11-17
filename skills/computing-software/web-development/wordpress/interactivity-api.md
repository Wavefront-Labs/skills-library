---
id: computing-software.web-development.wordpress.interactivity-api
name: interactivity-api
category: computing-software
field: web-development
product: wordpress
tags: [gutenberg-blocks, block-development, interactivity-api, data-wp-interactive, wordpress-interactivity, store-api, server-side-state, view-script-module]
level: practitioner
status: docs-checked
description: "Adding front-end interactivity to blocks with the WordPress Interactivity API: directives, store state/actions, server-side state hydration and viewScriptModule."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/interactivity-api/directives-and-store.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/interactivity-api/core-concepts/server-side-rendering.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/interactivity-api/core-concepts/client-side-navigation.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/interactivity-api/iapi-quick-start-guide.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interactivity API

Requires WordPress 6.5 or later.

**Goal:** interactive block front ends (toggles, carousels, filters, cart counters) using a standard WordPress system instead of ad-hoc jQuery, server-rendered first.

## 1. Opt in
```json
// block.json
{ "supports": { "interactivity": true }, "viewScriptModule": "file:./view.js", "render": "file:./render.php" }
```

## 2. Server render with directives
```php
<?php
wp_interactivity_state( 'acme/faq', [ 'openCount' => 0 ] );
$context = [ 'isOpen' => false ];
?>
<div <?php echo get_block_wrapper_attributes(); ?> data-wp-interactive="acme/faq" <?php echo wp_interactivity_data_wp_context( $context ); ?>>
  <button data-wp-on--click="actions.toggle" data-wp-bind--aria-expanded="context.isOpen"><?php echo esc_html( $attributes['question'] ); ?></button>
  <div data-wp-bind--hidden="!context.isOpen"><?php echo wp_kses_post( $content ); ?></div>
  <p data-wp-text="state.openLabel"></p>
</div>
```
With `supports.interactivity` set, WordPress processes the directives on the server (`wp_interactivity_process_directives`, built on the HTML API), so the initial HTML already reflects state.

## 3. Store
```js
// view.js (ES module)
import { store, getContext } from '@wordpress/interactivity';
const { state } = store('acme/faq', {
  state: { get openLabel() { return `${state.openCount} open`; } },
  actions: {
    toggle() { const ctx = getContext(); ctx.isOpen = !ctx.isOpen; state.openCount += ctx.isOpen ? 1 : -1; },
  },
});
```
- **State** is global per namespace; **context** is local to an element subtree (each FAQ item).
- Directives: `data-wp-on--event`, `data-wp-bind--attr`, `data-wp-class--name`, `data-wp-text`, `data-wp-each`, `data-wp-watch`, `data-wp-init`. Handlers run asynchronously by default; an action that needs synchronous access to the `event` object must be wrapped in `withSyncEvent()`.
- Derived state with getters; async actions as generator functions (`*fetchMore() { const r = yield fetch(...) }`).
- Shared namespaces let blocks talk to each other (mini-cart + add-to-cart button).

## 4. Notes
- Client-side navigation uses the `@wordpress/interactivity-router` package (bundled with core since 6.5): mark regions with `data-wp-router-region` and add the router as a dependency of your script module.
- Derived state defined with a client getter is not available on the server: initialise its value with `wp_interactivity_state()` or the server-rendered HTML (for example a `hidden` attribute) will be wrong.

## Verify
- [ ] Page source contains rendered state (correct `hidden`, `aria-expanded`) before JS runs.
- [ ] Interactions work on multiple block instances independently (context).
- [ ] No jQuery dependency.

## Checked

2026-10-25: against the Gutenberg trunk Interactivity API docs (last commit 2026-10-25). Confirmed: 6.5 minimum, `supports.interactivity`, `wp_interactivity_state`, `wp_interactivity_data_wp_context`, server directive processing, directive names including `data-wp-each`, generator-based async actions, `withSyncEvent`, router package and `data-wp-router-region`, derived-state server initialisation. Removed the unconfirmed claims that view modules load only on pages with the block and that the router handles query-loop pagination.

Method: documentation only; no commands were run.
