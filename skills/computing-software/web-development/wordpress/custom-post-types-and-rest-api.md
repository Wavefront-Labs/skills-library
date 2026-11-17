---
id: computing-software.web-development.wordpress.custom-post-types-and-rest-api
name: custom-post-types-and-rest-api
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, custom-post-type, taxonomy, rest-api, register_post_type, acf, headless-wordpress, php, web-development, custom-taxonomies]
level: advanced
status: docs-checked
description: "WordPress custom post types/taxonomies done right, and exposing/extending them in the REST API for headless or JS-driven frontends."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/post.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/meta.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/rest-api.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/rewrite.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/user.php
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WordPress custom post types, taxonomies, and the REST API

**Goal:** model content as its own type instead of overloading Pages/Posts
with categories as a workaround, and expose it correctly to a REST consumer
(a headless frontend, a mobile app, a JS widget) without leaking admin-only
fields.

## 1. Register the post type in a plugin, not the theme
```php
register_post_type('event', [
  'labels' => ['name' => 'Events', 'singular_name' => 'Event'],
  'public' => true,
  'show_in_rest' => true,          // without this, invisible to the REST API entirely
  'rest_base' => 'events',
  'supports' => ['title', 'editor', 'thumbnail', 'custom-fields'],
  'has_archive' => true,
  'rewrite' => ['slug' => 'events'],
]);
```
Register custom post types/taxonomies from a plugin (even a small
site-specific one), not the active theme: a post type registered in
`functions.php` stops being registered when someone switches themes, so its
content becomes unreachable until it is registered again. Hook registration to
`init`, and flush rewrite rules once on activation (`flush_rewrite_rules()` in
the plugin's activation hook, after registering the type) rather than on every request.

## 2. Taxonomies — hierarchical vs flat, and when to use a custom one at all
```php
register_taxonomy('event_category', 'event', ['hierarchical' => true, 'show_in_rest' => true]);
```
Hierarchical (like categories — parent/child) for genuine groupings;
non-hierarchical (like tags — flat, free-form) for attributes. Prefer a custom taxonomy scoped to
the CPT over the built-in `category`/`post_tag` for its own classification, so
unrelated content types' terms are not mixed together.

## 3. Exposing custom fields in the REST API
`'supports' => ['custom-fields']` alone does not put meta fields into the
REST response — register each meta key explicitly:
```php
register_post_meta('event', 'event_date', [
  'type' => 'string', 'single' => true, 'show_in_rest' => true,
  'auth_callback' => fn() => current_user_can('edit_posts'),
]);
```
Without `show_in_rest`, a registered meta key is not exposed to REST
consumers even though it is stored in the postmeta table. The post type must
also support `custom-fields`. For values that are not plain meta, a
`register_rest_field( $object_type, $attribute, $args )` callback can add them
to the response.

## 4. Custom REST endpoints beyond CRUD
```php
add_action('rest_api_init', function () {
  register_rest_route('myplugin/v1', '/events/upcoming', [
    'methods' => 'GET',
    'callback' => fn($request) => get_upcoming_events(),
    'permission_callback' => '__return_true',   // explicit: public, intentionally
  ]);
});
```
`permission_callback` is required: since WordPress 5.5.0 core raises a
`_doing_it_wrong()` notice when it is missing. Setting `__return_true` on
something that should not be public is the main security footgun here; always
set it deliberately.

## 5. Headless WordPress considerations
If the frontend is a separate JS app consuming this as a data source:
set `show_in_rest` consistently across every content type the frontend
depends on, and handle preview/draft content explicitly. Cookie authentication
needs a `wp_rest` nonce, which a separate-origin frontend does not have; use
Application Passwords (available on SSL sites or a `local` environment type) or
an authentication plugin for authenticated requests.

## Verify
- [ ] Custom post types/taxonomies are registered in a plugin, not the theme, and rewrite rules flush only on activation.
- [ ] `show_in_rest` is set on every CPT, taxonomy, and meta field the frontend needs — verified by actually calling the REST endpoint, not assumed from admin visibility.
- [ ] Every custom REST route has an explicit, deliberate `permission_callback`.
- [ ] A headless setup uses Application Passwords or an authentication plugin, not cookie auth.

## Checked

2026-10-25: against wordpress-develop trunk source (`post.php`, `meta.php`, `rest-api.php`, `rewrite.php`, `user.php`; last commit 2026-10-25). Confirmed: `show_in_rest` and `rest_base` post type arguments, `custom-fields` support requirement for registered meta in REST, `register_rest_field` signature, `permission_callback` notice since 5.5.0, `flush_rewrite_rules( $hard )`, Application Passwords availability. Removed unconfirmed claims: ACF REST settings, measurable performance cost of flushing, JWT and CORS advice, data-loss wording.

Method: documentation only; no commands were run.
