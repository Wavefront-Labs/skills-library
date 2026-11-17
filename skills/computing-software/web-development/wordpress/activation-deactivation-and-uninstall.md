---
id: computing-software.web-development.wordpress.activation-deactivation-and-uninstall
name: activation-deactivation-and-uninstall
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, activation-hooks, uninstall-php, register-activation-hook, plugin-lifecycle, dbdelta, php, web-development, wordpress-plugins, plugin-development]
level: practitioner
status: docs-checked
description: "Handling the WordPress plugin lifecycle: activation tasks and requirement checks, deactivation cleanup, uninstall.php data removal, multisite handling and upgrade routines."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/plugin.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-admin/includes/plugin.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-admin/includes/upgrade.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/ms-site.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-site-query.php
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Activation, deactivation and uninstall

**Goal:** plugins that set themselves up once, pause cleanly, and leave no data behind when deleted - without destroying data on a mere deactivation.

## 1. What goes where
| Hook | Do | Don't |
|---|---|---|
| Activation | create tables/options, add capabilities, schedule cron, flush rewrite rules after registering CPTs | output anything, long migrations |
| Deactivation | clear cron events, flush rewrite rules | delete user data |
| Uninstall | delete options, tables, post meta, user meta, transients, files | run when only deactivated |

## 2. Activation
```php
register_activation_hook( __FILE__, 'acme_activate' );
function acme_activate( $network_wide ) {
    if ( version_compare( PHP_VERSION, '8.1', '<' ) ) {
        deactivate_plugins( plugin_basename( __FILE__ ) );
        wp_die( esc_html__( 'Acme requires PHP 8.1+.', 'acme' ) );
    }
    acme_install_schema();
    acme_register_post_types();          // same function hooked to init
    flush_rewrite_rules();               // only here and on deactivation, never on every request
    add_option( 'acme_db_version', ACME_DB_VERSION );
}
```
`register_activation_hook( $file, $callback )` hooks the `activate_{plugin path}` action, so the callback runs when the plugin is activated, not on every request or update; register it at load time in the main plugin file with `__FILE__`. `register_deactivation_hook` works the same way for `deactivate_{plugin path}`.

## 3. Upgrades without activation
```php
add_action( 'plugins_loaded', function () {
    if ( get_option( 'acme_db_version' ) !== ACME_DB_VERSION ) {
        acme_install_schema();           // dbDelta is idempotent
        update_option( 'acme_db_version', ACME_DB_VERSION );
    }
} );
```
`dbDelta( $queries, $execute )` lives in `wp-admin/includes/upgrade.php`, so `require_once ABSPATH . 'wp-admin/includes/upgrade.php';` first. It compares each `CREATE TABLE` statement with the existing table; it recognises `PRIMARY KEY`, `UNIQUE`/`FULLTEXT`/`SPATIAL` keys and `KEY`/`INDEX` (`INDEX` is standardised to `KEY`).

## 4. Uninstall
```php
// uninstall.php (core includes it, with WP_UNINSTALL_PLUGIN defined, when the plugin is deleted)
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) exit;
delete_option( 'acme_options' );
delete_option( 'acme_db_version' );
delete_metadata( 'post', 0, '_acme_meta', '', true );       // all posts
global $wpdb;
$wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}acme_logs" );
wp_clear_scheduled_hook( 'acme_sync' );
```
Offer a "keep data on uninstall" setting for plugins holding valuable user content.

## 5. Multisite
`$network_wide` is true for network activation; loop sites (`get_sites( [ 'fields' => 'ids', 'number' => 0 ] )`, since `number` defaults to 100, with `switch_to_blog()`/`restore_current_blog()`); on large networks defer per-site setup instead. The `wp_initialize_site` action fires when a new site is created. Uninstall must clean every site.

## Verify
- [ ] Activate, deactivate, reactivate: no duplicate cron events or errors; data intact.
- [ ] Delete plugin: its options and custom tables are gone.
- [ ] Updating the plugin runs schema upgrades without reactivation (version-option check).

## Checked

2026-10-25: against wordpress-develop trunk source (`plugin.php`, `wp-admin/includes/plugin.php`, `upgrade.php`, `ms-site.php`, `class-wp-site-query.php`; last commit 2026-10-25). Confirmed: `register_activation_hook`/`register_deactivation_hook` hook names, `uninstall.php` loading with `WP_UNINSTALL_PLUGIN`, `dbDelta` signature and its handling of key types (`INDEX` standardised to `KEY`), `get_sites` `fields` and `number` (default 100), `wp_initialize_site`. Removed unconfirmed claims: update and mu-plugin non-firing, dbDelta field-per-line and lowercase rules, the preference for uninstall.php over the hook, and the WP-CLI check.

Method: documentation only; no commands were run.
