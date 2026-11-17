---
id: computing-software.web-development.wordpress.block-bindings-api
name: block-bindings-api
category: computing-software
field: web-development
product: wordpress
tags: [block-bindings, post-meta-binding, block-editor, custom-fields, wordpress]
level: advanced
status: docs-checked
description: "Binding core block attributes to dynamic data with the Block Bindings API: post meta, custom sources in PHP and JS, supported blocks, editing and limits."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/block-api/block-bindings.md
  - https://developer.wordpress.org/block-editor/reference-guides/block-api/block-bindings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block Bindings API

Introduced in WordPress 6.5: bind attributes of core blocks to dynamic sources (post meta, custom PHP callbacks) without writing custom blocks.

## 1. Supported blocks and attributes
Default list: Image (`id`, `url`, `title`, `alt`, `caption`), Heading (`content`), Paragraph (`content`), Button (`url`, `text`, `linkTarget`, `rel`), Navigation Link and Navigation Submenu (`url`), Post Date (`datetime`). Since WordPress 6.9 the `block_bindings_supported_attributes` filter (and the per-block `block_bindings_supported_attributes_{$block_type}` filter) adds attributes; Pattern Overrides share the same list.

## 2. Binding post meta
```php
register_post_meta( 'book', 'isbn', [ 'show_in_rest' => true, 'single' => true, 'type' => 'string',
    'sanitize_callback' => 'sanitize_text_field', 'auth_callback' => fn() => current_user_can( 'edit_posts' ) ] );
```
```html
<!-- wp:paragraph {"metadata":{"bindings":{"content":{"source":"core/post-meta","args":{"key":"isbn"}}}}} -->
<p></p>
<!-- /wp:paragraph -->
```
- Meta must be registered with `show_in_rest` true; keys that start with an underscore are protected and cannot be used with Block Bindings.
- The `core/post-meta` source is a core source; core also ships `core/pattern-overrides` and (since 6.9) `core/term-data`.
- In templates (Site Editor) the value comes from the post being displayed - great for single templates of custom post types.

## 3. Custom sources
```php
add_action( 'init', function () {
    register_block_bindings_source( 'acme/site-data', [
        'label'              => __( 'Site data', 'acme' ),
        'get_value_callback' => function ( array $args, WP_Block $block ) {
            return match ( $args['key'] ?? '' ) {
                'support_phone' => get_option( 'acme_support_phone' ),
                'year'          => gmdate( 'Y' ),
                default         => null,
            };
        },
        'uses_context' => [ 'postId', 'postType' ],
    ] );
} );
```
For editor previews register the same source in JS with `registerBlockBindingsSource( { name: 'acme/site-data', getValues(...) } )` from `@wordpress/blocks` (6.7+; JS option names are `name`, `label`, `usesContext`, `getValues`, and since 6.9 `getFieldsList`), so the editor can show values; a label set in JS overrides the PHP label.

## 4. Pattern overrides
Synced patterns use the `core/pattern-overrides` source to let specific blocks inside a synced pattern have per-instance content; each instance stores its override values in its `content` attribute.

## 5. Limits
Bound values are rendered into the block's HTML on the server. Not every attribute or block is supported; for complex layouts or logic build a dynamic block instead.

## Verify
- [ ] Bound blocks show the meta value on the front end and in the editor; custom source returns null safely for unknown keys.

## Checked

2026-10-25: against the Gutenberg trunk docs for Block Bindings (repository last commit 2026-10-25). Confirmed: compatible blocks and attributes table, protected-key and `show_in_rest` rule, `block_bindings_supported_attributes` filters (6.9), `uses_context`, `registerBlockBindingsSource` options, `core/pattern-overrides` behaviour. Removed unconfirmed claims about a sidebar bindings UI and inline editing, and the `render_block` escaping claim.

Method: documentation only; no commands were run.
