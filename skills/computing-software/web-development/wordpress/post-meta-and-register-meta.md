---
id: computing-software.web-development.wordpress.post-meta-and-register-meta
name: post-meta-and-register-meta
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, post-meta, register-meta, register-post-meta, metadata-api, rest-api, block-editor, php, web-development]
level: practitioner
status: docs-checked
description: "Storing custom fields in WordPress: register_post_meta with types, sanitisation, auth and REST exposure, meta boxes vs block editor sidebars, and meta query performance."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/meta.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/post.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-query.php
  - https://developer.wordpress.org/reference/functions/register_post_meta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post meta and register_meta

**Goal:** typed, validated custom fields available in PHP, REST and the block editor, without slow meta queries.

## 1. Register the meta
```php
add_action( 'init', function () {
    register_post_meta( 'event', 'acme_starts_at', [
        'type'              => 'string',
        'single'            => true,
        'default'           => '',
        'sanitize_callback' => fn( $v ) => preg_match( '/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/', $v ) ? $v : '',
        'auth_callback'     => fn( $allowed, $key, $post_id ) => current_user_can( 'edit_post', $post_id ),
        'show_in_rest'      => true,                       // required for block editor access
        'revisions_enabled' => true,                       // WP 6.4.0+, post meta only
    ] );
    register_post_meta( 'event', 'acme_capacity', [ 'type' => 'integer', 'single' => true, 'show_in_rest' => true,
        'sanitize_callback' => 'absint', 'auth_callback' => fn() => current_user_can( 'edit_posts' ) ] );
} );
```
The post type must declare support for `custom-fields` for registered meta to be accessible via REST. Complex values take `show_in_rest` as an array with `schema` or `prepare_callback` keys (for example `[ 'schema' => [ 'type' => 'object', 'properties' => [...] ] ]`). Valid `type` values are string, boolean, integer, number, array and object.
Prefix keys with `_` (`_acme_internal`) to mark them protected and hide them from the classic Custom Fields box; `auth_callback` is used for the edit, add and delete meta capability checks.

## 2. Read and write
```php
$start = get_post_meta( $post_id, 'acme_starts_at', true );   // single => true returns a scalar
update_post_meta( $post_id, 'acme_capacity', 50 );
delete_post_meta( $post_id, 'acme_capacity' );
```
`WP_Query` primes the post meta cache for its results by default (`update_post_meta_cache` defaults to true).

## 3. Editing UI
- Block editor: a `PluginDocumentSettingPanel` using `useEntityProp( 'postType', 'event', 'meta' )`, or block bindings (6.5+, `core/post-meta` source; keys starting with an underscore are not usable) to connect block attributes to meta.
- Classic meta box: `add_meta_box` + `save_post_event` handler with nonce, capability check, `DOING_AUTOSAVE` guard and sanitisation.

## 4. Query performance
`meta_query` joins the `postmeta` table (key/value rows). Fine for small sites; it can get slow on large ones, especially range comparisons and sorting on meta values.
- Filter on things that should be taxonomies (e.g. "type", "city") with taxonomies instead.
- High-volume structured data -> custom table.
- Set the `type` of a `meta_query` clause (for example `NUMERIC` or `DATETIME`) for correct comparisons; store dates as sortable strings (ISO 8601) or timestamps.

## 5. Other object types
`register_term_meta`, `register_meta( 'user', ... )`, `register_meta( 'comment', ... )` follow the same pattern.

## Verify
- [ ] `GET /wp-json/wp/v2/event/<id>` includes `meta.acme_starts_at`; an Author can't update another user's event meta.
- [ ] Invalid values are sanitised on save via REST and PHP.
- [ ] No slow meta queries on archive pages (check with a query logger).

## Checked

2026-10-25: against wordpress-develop trunk source (`meta.php`, `post.php`, `class-wp-query.php`; last commit 2026-10-25). Confirmed: `register_meta` argument list and defaults (`type` values, `single`, `default`, `sanitize_callback`, `auth_callback`, `show_in_rest` array form, `revisions_enabled` since 6.4.0 and post-only), the `custom-fields` support requirement for REST, `update_post_meta_cache` default true. Removed unconfirmed claims about the LONGTEXT column and a per-post meta query.

Method: documentation only; no commands were run.
