---
id: computing-software.web-development.wordpress.roles-and-capabilities
name: roles-and-capabilities
category: computing-software
field: web-development
product: wordpress
tags: [wordpress-capabilities, add-role, current-user-can, map-meta-cap, custom-post-type-capabilities, wordpress]
level: practitioner
status: docs-checked
description: "WordPress roles and capabilities: checking capabilities not roles, meta capabilities with map_meta_cap, custom post type caps, adding roles on activation only and cleaning up."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/capabilities.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/post.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-roles.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/plugin.php
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Roles and capabilities

## 1. Check capabilities, never role names
```php
if (current_user_can('edit_post', $post_id)) { ... }     // meta cap: resolves ownership, status, post type
if (current_user_can('manage_options')) { ... }           // primitive cap
// wrong: in_array('administrator', wp_get_current_user()->roles)
```
Roles are bundles of capabilities that sites customise; checking role names breaks on custom roles and multisite (super admins).

## 2. Meta capabilities
`edit_post`, `delete_post`, `read_post`, `edit_user`, `edit_comment` and similar take an object id and are mapped by `map_meta_cap` to primitive caps (`edit_posts`, `edit_others_posts`, `edit_published_posts`...). Customise mapping:
```php
add_filter('map_meta_cap', function ($caps, $cap, $user_id, $args) {
  if ($cap === 'edit_post' && get_post_type($args[0]) === 'invoice' && get_post_meta($args[0], '_locked', true)) {
    return ['do_not_allow'];
  }
  return $caps;
}, 10, 4);
```

## 3. Custom post type capabilities
```php
register_post_type('event', [
  'capability_type' => ['event', 'events'],   // edit_event, edit_events, edit_others_events, publish_events...
  'map_meta_cap'    => true,                    // default is false
  // ...
]);
```
Then grant the new primitive caps to roles that should manage events.

## 4. Adding roles and caps (activation only)
```php
register_activation_hook(__FILE__, function () {
  add_role('event_manager', 'Event Manager', ['read' => true, 'edit_events' => true, 'publish_events' => true]);
  get_role('administrator')->add_cap('edit_events');
});
register_uninstall_hook(__FILE__, 'myplugin_uninstall');   // remove_role / remove_cap there
```
Roles and caps are stored in the database (the `{prefix}user_roles` option, read through `WP_Roles`); calling `add_role`/`add_cap` on every request is wasteful and hides bugs.

## 5. Everywhere permissions matter
Admin pages (`add_menu_page` capability argument plus a check in the handler), AJAX/`admin-post` handlers, REST `permission_callback` and block editor UI. Nonces prove intent, not permission: always pair them with `current_user_can`.

## Verify
- [ ] A user with the custom role can do exactly the intended actions (test each REST/AJAX endpoint as that user and as a subscriber).

## Checked

2026-10-25: against wordpress-develop trunk source (`capabilities.php`, `post.php`, `class-wp-roles.php`, `plugin.php`; last commit 2026-10-25). Confirmed: `map_meta_cap` returns `do_not_allow` for blocked meta caps, `capability_type` accepts an array of singular and plural and defaults to 'post', `map_meta_cap` default false, roles stored under `{prefix}user_roles`, `register_activation_hook` and `register_uninstall_hook` signatures. Removed the unconfirmed `canUser` reference.

Method: documentation only; no commands were run.
