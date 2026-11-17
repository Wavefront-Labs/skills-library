---
id: computing-software.web-development.wordpress.functions-php-theme-supports-and-nav-menus
name: functions-php-theme-supports-and-nav-menus
category: computing-software
field: web-development
product: wordpress
tags: [add-theme-support, nav-menus, functions-php, classic-themes, wordpress]
level: practitioner
status: docs-checked
description: "Classic theme setup in functions.php: after_setup_theme, add_theme_support options, registering and rendering nav menus, widget areas, and keeping logic in plugins."
sources:
  - https://developer.wordpress.org/themes/basics/theme-functions/
  - https://developer.wordpress.org/reference/functions/add_theme_support/
  - https://developer.wordpress.org/themes/functionality/navigation-menus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# functions.php, theme supports and nav menus

## 1. Theme setup
```php
add_action( 'after_setup_theme', 'acme_setup' );
function acme_setup() {
    load_theme_textdomain( 'acme', get_template_directory() . '/languages' );
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'html5', [ 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'navigation-widgets' ] );
    add_theme_support( 'custom-logo', [ 'height' => 80, 'width' => 240 ] );
    add_theme_support( 'responsive-embeds' );
    add_theme_support( 'editor-styles' ); add_editor_style( 'assets/editor.css' );
    add_theme_support( 'wp-block-styles' );
    register_nav_menus( [ 'primary' => __( 'Primary menu', 'acme' ), 'footer' => __( 'Footer menu', 'acme' ) ] );
}
```
- Hook into `after_setup_theme`; the `init` hook may be too late for some features (add_theme_support reference).
- A classic theme can opt into `theme.json` for editor settings without becoming a block theme.

## 2. Rendering menus
```php
wp_nav_menu( [
    'theme_location' => 'primary',
    'fallback_cb'    => false,       // do not fall back to a Page menu when no menu is assigned
] );
```
Use `theme_location` and `fallback_cb` so an unassigned location does not fall back to the first non-empty menu or a Page menu (Navigation Menus handbook).

## 3. Widgets and sidebars
Register sidebars with `register_sidebar()` or `register_sidebars()`, not with `add_theme_support` (add_theme_support reference).

## 4. What doesn't belong in functions.php
Custom post types, shortcodes, integrations and anything content depends on: put them in a plugin (or mu-plugin) so switching themes doesn't lose functionality. Theme = presentation.

## Verify
- [ ] Menus render only for assigned locations; CPTs live in a plugin.

## Checked

2026-10-28. Confirmed from the add_theme_support reference (must be called from functions.php and, if hooked, on `after_setup_theme`; `init` may be too late; `title-tag`, `post-thumbnails`, `responsive-embeds`, `editor-styles`, `wp-block-styles`, `custom-logo` with `height`/`width`, `html5` with `navigation-widgets`; sidebars via `register_sidebar()`, menus via `register_nav_menus()`), the Theme Functions handbook and the Navigation Menus handbook (`theme_location`, `fallback_cb`). Corrected: the `html5` arguments `style` and `script` are deprecated and unused since WordPress 7.0.0, so they were removed. Removed (not found): `add_image_size`, `container_aria_label`, `depth`, `has_nav_menu`, aria-current and WCAG menu claims, widget-area code, Theme Check.

Method: documentation only; no commands were run.
