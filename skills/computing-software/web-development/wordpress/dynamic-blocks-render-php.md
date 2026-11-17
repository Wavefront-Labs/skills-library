---
id: computing-software.web-development.wordpress.dynamic-blocks-render-php
name: dynamic-blocks-render-php
category: computing-software
field: web-development
product: wordpress
tags: [gutenberg-blocks, block-development, dynamic-blocks, render-php, server-side-render, render-callback, get-block-wrapper-attributes, latest-posts-block]
level: practitioner
status: docs-checked
description: "Building dynamic WordPress blocks rendered in PHP via render.php: when to choose them, attributes and context, get_block_wrapper_attributes, escaping and editor preview."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/getting-started/fundamentals/static-dynamic-rendering.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/how-to-guides/block-tutorial/creating-dynamic-blocks.md
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-metadata.md
  - https://developer.wordpress.org/reference/functions/get_block_wrapper_attributes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic blocks with render.php

**Goal:** blocks whose output is computed on each request (latest posts, user-specific content, data from options/APIs) and can change markup without block validation errors.

## 1. When dynamic
Choose dynamic when output depends on data that changes after the post is saved, or when you expect to change the markup later (static blocks need deprecations for every markup change). Static is fine for pure content blocks.

## 2. Setup
```json
// block.json
{ "name": "acme/recent-projects", "attributes": { "count": { "type": "number", "default": 3 } },
  "render": "file:./render.php", "usesContext": ["postId"], "supports": { "align": true, "color": { "text": true } } }
```
```js
// save.js - return null (nothing stored but the comment delimiter + attributes)
export default function save() { return null; }
```
```php
<?php // render.php - $attributes, $content, $block are in scope
$q = new WP_Query( [ 'post_type' => 'project', 'posts_per_page' => absint( $attributes['count'] ), 'no_found_rows' => true ] );
if ( ! $q->have_posts() ) { return; }
?>
<ul <?php echo get_block_wrapper_attributes( [ 'class' => 'recent-projects' ] ); ?>>
  <?php while ( $q->have_posts() ) : $q->the_post(); ?>
    <li><a href="<?php the_permalink(); ?>"><?php echo esc_html( get_the_title() ); ?></a></li>
  <?php endwhile; wp_reset_postdata(); ?>
</ul>
```
- `get_block_wrapper_attributes()` outputs classes/styles from supports (colour, alignment, custom class) - without it, those settings silently don't apply.
- Escape everything (`esc_html`, `esc_url`, `esc_attr`, `wp_kses_post`).
- `no_found_rows` skips the pagination count query.

## 3. Editor preview
- `<ServerSideRender block="acme/recent-projects" attributes={attributes} />` from `@wordpress/server-side-render` renders the PHP output on the server for the editor - easy, but a round trip per change.
- Better: render a JS preview using core data (`useSelect( select => select('core').getEntityRecords('postType','project',{per_page: count}) )`).

## 4. Inner blocks in dynamic blocks
`save` returns `<InnerBlocks.Content />` so the inner blocks are stored; `$content` in render.php holds the markup of the block as stored in the database, including the inner blocks.

## Verify
- [ ] Changing render.php markup doesn't produce invalid-block warnings in existing posts.
- [ ] Alignment/colour supports appear on the front end.
- [ ] The block's queries are bounded (check with a query logger).

## Checked

2026-10-25: against the Gutenberg trunk docs (last commit 2026-10-25). Confirmed: `render` as `file:./render.php`, `$attributes`, `$content` and `$block` in scope, `save` returning null, `get_block_wrapper_attributes()`, `ServerSideRender` from `@wordpress/server-side-render`, `InnerBlocks.Content` in save for dynamic blocks. Removed unconfirmed REST wording, transient caching advice and the Query Monitor reference.

Method: documentation only; no commands were run.
