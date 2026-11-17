---
id: computing-software.web-development.wordpress.wp-cron-scheduling
name: wp-cron-scheduling
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, wp-cron, scheduled-events, disable-wp-cron, action-scheduler, wp-cli, php, web-development]
level: practitioner
status: docs-checked
description: "Scheduling background work in WordPress: wp_schedule_event, custom intervals, unscheduling on deactivation, DISABLE_WP_CRON with system cron, and Action Scheduler."
sources:
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/cron.php
  - https://github.com/wp-cli/cron-command/blob/main/README.md
  - https://github.com/woocommerce/action-scheduler/blob/trunk/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WP-Cron scheduling

**Goal:** recurring and one-off jobs that run reliably, once, and are cleaned up when the plugin is removed.

## 1. How WP-Cron works
Not a real cron: on page loads WordPress checks for due events and spawns a non-blocking request (`spawn_cron()` posts with `blocking` false) to `wp-cron.php`, guarded by a lock (`WP_CRON_LOCK_TIMEOUT`). Events therefore only run when the site receives visits, and anything that blocks that request stops it.

## 2. Schedule a recurring event
```php
register_activation_hook( __FILE__, function () {
    if ( ! wp_next_scheduled( 'acme_sync' ) ) {
        wp_schedule_event( time() + 60, 'hourly', 'acme_sync' );
    }
} );
add_action( 'acme_sync', 'acme_run_sync' );
register_deactivation_hook( __FILE__, function () {
    wp_clear_scheduled_hook( 'acme_sync' );
} );
```
Always guard with `wp_next_scheduled` - scheduling on every `init` without it creates duplicates. Built-in recurrences: `hourly`, `twicedaily`, `daily` and `weekly`; add more with the `cron_schedules` filter. Since WordPress 5.7 the scheduling functions take a `$wp_error` parameter and can return a `WP_Error`.

## 3. Custom intervals and single events
```php
add_filter( 'cron_schedules', function ( $s ) {
    $s['every_five_minutes'] = [ 'interval' => 5 * MINUTE_IN_SECONDS, 'display' => __( 'Every 5 minutes', 'acme' ) ];
    return $s;
} );
wp_schedule_single_event( time() + 30, 'acme_send_receipt', [ $order_id ] );   // args become part of the event identity
```
The `cron_schedules` filter must be registered on every request (not only on activation), or WordPress can't reschedule the event.

## 4. Use real cron in production
```php
// wp-config.php: stops WordPress spawning cron on page loads
define( 'DISABLE_WP_CRON', true );
```
```bash
*/5 * * * * cd /var/www/site && wp cron event run --due-now --quiet
```
Multisite: run the same command once per site with `--url=<site url>` (`wp site list --field=url` lists the URLs).

## 5. Long or many jobs: Action Scheduler
WP-Cron stores all events in a single option (`cron`, saved with autoload on). Action Scheduler is a separate job-queue library, distributed inside plugins, for large or traceable background workloads:
```php
as_enqueue_async_action( 'acme_process_order', [ 'order_id' => $id ], 'acme' );        // $hook, $args, $group
as_schedule_recurring_action( time(), HOUR_IN_SECONDS, 'acme_sync', [], 'acme' );   // $timestamp, $interval_in_seconds, $hook, $args, $group
```

## 6. Job hygiene
Make handlers idempotent and process in batches so one run cannot overlap the next.

## Verify
- [ ] `wp cron event list` shows exactly one `acme_sync` event with the right recurrence.
- [ ] Deactivating the plugin removes its events.
- [ ] Events run on schedule with `DISABLE_WP_CRON` and system cron (`wp cron test` checks that WP-Cron can run).

## Checked

2026-10-25: against wordpress-develop trunk `cron.php`, the wp-cli cron-command README and the Action Scheduler API doc (last commits 2026-10-25). Confirmed: built-in recurrences and `cron_schedules` filter, `spawn_cron` non-blocking request and lock, `DISABLE_WP_CRON`, `cron` option saved with autoload, `wp_schedule_event`/`wp_schedule_single_event`/`wp_clear_scheduled_hook`/`wp_next_scheduled` signatures, `wp cron event run --due-now` and `wp cron test`, `as_enqueue_async_action` and `as_schedule_recurring_action` signatures. Removed unconfirmed claims about retries/logging absence, the curl alternative, a WooCommerce bundle, and the transient-lock snippet.

Method: documentation only; no commands were run.
