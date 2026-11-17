---
id: computing-software.web-development.wordpress.autoloaded-options-and-database-cleanup
name: autoloaded-options-and-database-cleanup
category: computing-software
field: web-development
product: wordpress
tags: [autoloaded-options, database-cleanup, wp-options, post-revisions, wordpress]
level: advanced
status: docs-checked
description: "Keeping the WordPress database lean: bloated autoloaded options, 6.6+ autoload values, expired transients, revisions, orphaned meta and WP-CLI cleanup."
sources:
  - https://make.wordpress.org/core/2024/06/18/options-api-disabling-autoload-for-large-options/
  - https://developer.wordpress.org/cli/commands/option/set-autoload/
  - https://developer.wordpress.org/reference/functions/wp_set_options_autoload/
  - https://developer.wordpress.org/cli/commands/transient/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoloaded options and database cleanup

## 1. Why autoload matters
On every request WordPress loads all options with autoload enabled in one query and keeps them in memory/object cache. Plugins that store large blobs (logs, caches, serialized settings) as autoloaded options slow every page.

## 2. Find the offenders
```bash
wp option list --autoload=on --format=total_bytes
wp db query "SELECT option_name, LENGTH(option_value) AS bytes, autoload FROM $(wp db prefix)options
  WHERE autoload IN ('yes','on','auto-on','auto') ORDER BY bytes DESC LIMIT 20;"
```
Site Health (6.6+) warns when autoloaded options exceed ~800 KB.

## 3. Autoload values (WordPress 6.6+)
`autoload` column now uses `on`/`off` (explicit), `auto-on`/`auto-off` (WordPress decided), and `auto` (default). Options larger than 150 KB (filterable via `wp_max_autoloaded_option_size`) are no longer autoloaded by default.
```php
add_option( 'acme_cache_blob', $data, '', false );                  // never autoload big or rarely used data
update_option( 'acme_settings', $settings, true );                   // small, used every request
wp_set_options_autoload( [ 'old_plugin_log', 'old_plugin_cache' ], false );   // 6.4+ bulk change
```
```bash
wp option set-autoload old_plugin_log off      # WP-CLI 2.8.0+
```

## 4. Other bloat
| Bloat | Cleanup |
|---|---|
| Expired transients (without object cache) | `wp transient delete --expired` |
| Leftover options from removed plugins | inspect prefixes, back up, `wp option delete` |
| Post revisions | cap them in configuration, then delete old revisions in batches after a backup |
| Orphaned postmeta | `DELETE pm FROM wp_postmeta pm LEFT JOIN wp_posts p ON p.ID = pm.post_id WHERE p.ID IS NULL` (after backup) |
| Spam/trash comments | delete in batches with WP-CLI `wp comment` |

## 5. Safety
Back up the database first, test on staging, delete in batches, and avoid one-click cleanup plugins that drop data you can't identify. After cleanup, flush the object cache and recheck the autoloaded total.

## Checked
2026-10-31. Confirmed against the WordPress 6.6 Options API dev note (autoload values, 150000-byte threshold and `wp_max_autoloaded_option_size`, 800 KB Site Health check), `wp_set_options_autoload()` (introduced 6.4.0), and WP-CLI `option list` (`--format=total_bytes`), `option set-autoload` (available since WP-CLI 2.8.0, corrected from 2.10+) and `transient delete`. Removed: the Memcached 1 MB claim, the `WP_POST_REVISIONS` and revision-deletion one-liners, the Action Scheduler retention hook, and the revisions source (404).
Method: documentation only; no commands were run.

## Verify
- [ ] Autoloaded options total well under ~800 KB; no large rarely used options autoloaded; revisions capped; Site Health clear of autoload warnings.
