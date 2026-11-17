---
id: computing-software.web-development.wordpress.child-themes-plugins-and-hooks
name: child-themes-plugins-and-hooks
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, wp, php, child-theme, block-theme, theme-json, full-site-editing, fse, plugins, hooks, actions, filters, add-action, add-filter, wp-enqueue-script, wp-enqueue-style, custom-post-types, register-post-type, nonces, wp-nonce, sanitize, escaping, esc-html, capabilities, current-user-can, wpdb, prepared-statements, sql-injection, xss, csrf, wp-cli, cms, web-development]
level: practitioner
status: docs-checked
description: "Extending WordPress safely: child themes vs block themes, actions vs filters, enqueueing, custom post types, nonces, escaping, wpdb prepare, WP-CLI."
sources:
  - https://developer.wordpress.org/themes/
  - https://developer.wordpress.org/plugins/
  - https://developer.wordpress.org/apis/security/
  - https://developer.wordpress.org/cli/commands/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WordPress child themes, plugins and hooks — extend, never edit

**Goal:** customise a WordPress site so that core, theme and plugin updates never
overwrite your work, and every piece of custom code is secure by default.

## 1. Where code belongs
| Change | Put it in |
|---|---|
| Look and layout of a classic theme | Child theme |
| Colours, fonts, spacing of a block theme | `theme.json` (child theme or Site Editor styles) |
| Functionality that should survive a theme switch (CPTs, shortcodes, integrations) | A plugin (or `wp-content/mu-plugins/` for must-run site code) |
| Anything in `wp-admin/`, `wp-includes/` or a third-party plugin | **Nowhere** — the next update erases it. Use a hook. |

## 2. Child theme (classic parent)
`wp-content/themes/parent-child/style.css`:
```css
/*
Theme Name: Parent Child
Template: parent
*/
```
`functions.php`:
```php
add_action( 'wp_enqueue_scripts', function () {
    wp_enqueue_style( 'parent', get_template_directory_uri() . '/style.css' );
    wp_enqueue_style( 'child', get_stylesheet_uri(), [ 'parent' ], wp_get_theme()->get( 'Version' ) );
} );
```
`Template:` must be the parent's folder name exactly (case-sensitive). Copy a template file into the child to override it. The child's `functions.php` loads
**before** the parent's (it doesn't replace it). `get_template_directory()` = parent,
`get_stylesheet_directory()` = child.

**Block themes:** templates are HTML in `templates/` and `parts/`, styling lives in
`theme.json` (`settings` for presets like palette and font sizes, `styles` for applying
them).
Site Editor edits are stored in the database and override theme files — export them before
assuming a file change will show.

## 3. Actions vs filters
- **Action:** "something happened, do something" — return value ignored. `add_action( 'init', 'my_register_types' );`
- **Filter:** "here's a value, return it (possibly changed)" — **must return**, or the content vanishes.
```php
add_filter( 'the_content', function ( $content ) {
    if ( is_singular( 'post' ) ) { $content .= '<p class="cta">…</p>'; }
    return $content;                      // always
}, 20 );                                  // priority: default 10, higher runs later
```
To undo a parent/plugin hook, `remove_action()` with the same callback **and priority**,
from a hook that fires after it was added (e.g. `after_setup_theme` or `init`).

## 4. Assets
Never hard-code `<script>` tags in templates. Enqueue with dependencies and versions:
```php
wp_enqueue_script( 'my-app', plugins_url( 'build/app.js', __FILE__ ), [], '1.4.0',
    [ 'in_footer' => true, 'strategy' => 'defer' ] );   // array arg since WP 6.3
wp_localize_script( 'my-app', 'MyApp', [ 'nonce' => wp_create_nonce( 'wp_rest' ) ] );
```
Load admin assets on `admin_enqueue_scripts`, checking the `$hook_suffix` so they only load on your screen.

## 5. Custom post types
```php
add_action( 'init', function () {
    register_post_type( 'event', [
        'label' => 'Events', 'public' => true, 'has_archive' => true,
        'show_in_rest' => true,                       // required for the block editor
        'supports' => [ 'title', 'editor', 'thumbnail' ],
        'rewrite' => [ 'slug' => 'events' ],
    ] );
} );
register_activation_hook( __FILE__, 'flush_rewrite_rules' );  // never flush on every request
```
New CPT URLs 404 until rewrite rules flush (or Settings → Permalinks → Save).

## 6. Security: the four checks on every input
```php
if ( ! isset( $_POST['_mynonce'] ) || ! wp_verify_nonce( $_POST['_mynonce'], 'save_event' ) ) wp_die( 'Bad nonce' ); // CSRF
if ( ! current_user_can( 'edit_post', $post_id ) ) wp_die( 'Forbidden' );                                              // authorisation
$title = sanitize_text_field( wp_unslash( $_POST['title'] ) );                                                        // sanitise in
echo '<h2>' . esc_html( $title ) . '</h2><a href="' . esc_url( $link ) . '">';                                     // escape out
$rows = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->prefix}events WHERE venue = %s AND seats > %d", $venue, $min ) );                         // SQL
```
A nonce is not authorisation — always pair it with `current_user_can()`. Escape late, at
output, with the function matching the context (`esc_html`, `esc_attr`, `esc_url`,
`wp_kses_post`). REST routes need a real `permission_callback` (`'__return_true'` only for
genuinely public data).

## 7. WP-CLI
```bash
wp core update && wp plugin update --all && wp core update-db
wp search-replace 'https://old.example.com' 'https://example.com' --dry-run   # handles serialised data
wp scaffold child-theme parent-child --parent_theme=parent
wp cron event list; wp transient delete --all; wp rewrite flush
```
Never run raw SQL find-and-replace on URLs — it corrupts serialised PHP arrays.

## Verify
- [ ] No modified files in core or third-party plugins (`wp core verify-checksums`, `wp plugin verify-checksums --all`).
- [ ] Theme/plugin updates applied on staging without losing customisations.
- [ ] Every filter callback returns a value.
- [ ] Every form/AJAX/REST handler checks nonce + capability, sanitises input, escapes output, uses `prepare()`.
- [ ] Scripts are enqueued with versions; none print inline from templates.

## Checked

2026-11-02. Checked against developer.wordpress.org: the Child Themes handbook page (Template header must match the parent folder name, child themes load before parents, enqueueing the parent stylesheet), function references for wp_enqueue_script (in_footer and strategy arguments), wp_localize_script, add_filter, remove_action, register_post_type (show_in_rest), register_rest_route (permission_callback), wp_verify_nonce, wpdb::prepare, sanitize_text_field, wp_unslash, esc_url, wp_kses_post, wp_get_theme and is_singular; the Security API pages on validation, escaping and nonces; the Block Themes pages (user customisations override theme.json and templates); and WP-CLI command pages for core and plugin verify-checksums, search-replace (--dry-run), scaffold child-theme, transient delete, plugin update and core update-db. Removed the claim that a child block theme's partial theme.json merges over the parent's, which no fetched page states.

Method: documentation only; no commands were run.
