---
id: computing-software.web-development.wordpress.wp-debug-and-query-monitor
name: wp-debug-and-query-monitor
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, wp-debug, query-monitor, debugging, wp-debug-log, script-debug, php, web-development]
level: practitioner
status: docs-checked
description: "Debugging WordPress: WP_DEBUG, WP_DEBUG_LOG and WP_DEBUG_DISPLAY setup, SCRIPT_DEBUG, SAVEQUERIES, Query Monitor, environment types and safe production practice."
sources:
  - https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/
  - https://developer.wordpress.org/reference/functions/wp_get_environment_type/
  - https://developer.wordpress.org/cli/commands/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WP_DEBUG and Query Monitor

**Goal:** see errors, slow queries, hook order and HTTP calls in development without leaking anything in production.

## 1. wp-config.php constants
```php
// development
define( 'WP_ENVIRONMENT_TYPE', 'development' );     // local | development | staging | production
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );                     // wp-content/debug.log, or a path: '/var/log/wp/debug.log'
define( 'WP_DEBUG_DISPLAY', false );                // log, don't print into HTML/JSON responses
@ini_set( 'display_errors', 0 );
define( 'SCRIPT_DEBUG', true );                     // unminified core JS/CSS
define( 'SAVEQUERIES', true );                      // save each query with its time and caller
```
Use these tools in local development or staging, not on a production site: keep `WP_DEBUG` false there. `wp_get_environment_type()` returns local, development, staging or production (default production), so code can branch safely.

## 2. Query Monitor
Install the Query Monitor plugin on development or staging and use its panels for queries, PHP errors, hooks and outbound HTTP calls; see the plugin's own documentation for the panel list.

## 3. Logging your own diagnostics
```php
error_log( 'acme: sync started ' . wp_json_encode( [ 'count' => $n ] ) );
```

## 4. Find the culprit fast
- White screen / critical error: check `debug.log` and the PHP error log.
- `wp plugin deactivate --all` then reactivate one by one.
- WP-CLI: `wp eval 'var_dump( get_option( "acme_options" ) );'`, `wp cron event list`, `wp transient list`.

## Checked
2026-10-31. Confirmed against Debugging in WordPress (WP_DEBUG, WP_DEBUG_LOG incl. custom path, WP_DEBUG_DISPLAY default true, SCRIPT_DEBUG default false, SAVEQUERIES, dev/staging advice), `wp_get_environment_type()` (values and production default) and the WP-CLI pages for `eval`, `plugin deactivate`, `cron event list`, `transient list`. Removed: Query Monitor panel list, `x-qm-*` headers and `qm/*` hooks (the cited Query Monitor page 404s), the claim that debug.log is publicly downloadable, recovery-mode, Health Check and Xdebug remarks.
Method: documentation only; no commands were run.

## Verify
- [ ] `curl -I https://example.com/wp-content/debug.log` returns 403/404.
- [ ] Production has `WP_DEBUG_DISPLAY` false and no QM output for anonymous users.
- [ ] Development shows zero PHP notices from your plugin/theme in QM.
