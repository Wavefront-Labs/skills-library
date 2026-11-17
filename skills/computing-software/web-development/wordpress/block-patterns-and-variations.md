---
id: computing-software.web-development.wordpress.block-patterns-and-variations
name: block-patterns-and-variations
category: computing-software
field: web-development
product: wordpress
tags: [gutenberg-blocks, block-development, block-patterns, block-variations, register-block-pattern, synced-patterns, pattern-categories, patterns-directory]
level: practitioner
status: docs-checked
description: "Providing reusable layouts with block patterns (PHP files in /patterns, synced vs unsynced) and preconfigured blocks with block variations."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-patterns.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-variations.md
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-theme.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/block-patterns.php
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block patterns and variations

**Goal:** editors build pages from ready-made, on-brand layouts, and get preconfigured versions of blocks, with little custom code.

## 1. Patterns as files (themes)
```php
<?php
/**
 * Title: Hero with call to action
 * Slug: acme/hero-cta
 * Categories: banner, featured
 * Keywords: hero, header
 * Block Types: core/post-content
 * Viewport Width: 1280
 * Inserter: true
 */
?>
<!-- wp:cover {"dimRatio":50,"align":"full"} -->
<div class="wp-block-cover alignfull"> … <!-- wp:heading {"level":1} --><h1 class="wp-block-heading"><?php esc_html_e( 'Build faster', 'acme' ); ?></h1><!-- /wp:heading --> … </div>
<!-- /wp:cover -->
```
Files in a theme's `/patterns` directory register automatically. Build the layout in the editor, copy the block markup from the Code editor, and replace strings with translatable/escaped PHP. Plugins: `register_block_pattern( 'acme/hero-cta', [ 'title' => …, 'content' => … ] )` and `register_block_pattern_category`.

## 2. Synced vs unsynced
- **Unsynced** (default): inserted as a copy; editing one instance doesn't affect others.
- **Synced patterns** (formerly reusable blocks, `wp_block` post type): one source, every instance updates. Pattern overrides (the `core/pattern-overrides` bindings source) let specific blocks within a synced pattern vary per instance while the rest stays synced.
- The `Block Types` header (`blockTypes` in `register_block_pattern`) names the block types the pattern is intended for; other optional headers are `Post Types`, `Template Types`, `Description`, `Viewport Width`, `Inserter` (yes/no), `Categories` and `Keywords`.

## 3. Variations
```js
import { registerBlockVariation } from '@wordpress/blocks';
registerBlockVariation('core/group', {
  name: 'acme-notice', title: 'Notice', icon: 'info',
  attributes: { className: 'is-style-notice', backgroundColor: 'pale-cyan-blue' },
  innerBlocks: [['core/paragraph', { placeholder: 'Notice text…' }]],
  isActive: ['className'],
  scope: ['inserter', 'transform'],
});
```
Variations appear as their own inserter items; `isActive` lets the editor recognise them later. `scope` defaults to `block` and `inserter`; `isActive` may be an attribute-name array or a function. Block **styles** (`register_block_style`) are lighter: just a class choice.

## 4. Curation
Disable core/remote patterns if off-brand: `remove_theme_support( 'core-block-patterns' )` and `add_filter( 'should_load_remote_block_patterns', '__return_false' )`. Patterns registered with `register_block_pattern` must be registered on `init`; `unregister_block_pattern( $name )` removes one.

## Verify
- [ ] Patterns appear in the right categories and insert without invalid-block warnings.
- [ ] Strings in patterns are translatable and escaped.
- [ ] Variations show in the inserter and are recognised after save/reload.

## Checked

2026-10-25: against Gutenberg trunk docs (block patterns, block variations) and wordpress-develop trunk source (`WP_Theme::get_block_patterns` file header list, `block-patterns.php`), last commits 2026-10-25. Confirmed: pattern file header names, `core-block-patterns` theme support, `should_load_remote_block_patterns` filter, `register_block_pattern` options, variation `scope` values and `isActive` forms. Removed unconfirmed version gates (6.0, 6.6), the start-page modal claim and the core-variations claim.

Method: documentation only; no commands were run.
