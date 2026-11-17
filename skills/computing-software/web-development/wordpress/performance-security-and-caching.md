---
id: computing-software.web-development.wordpress.performance-security-and-caching
name: performance-security-and-caching
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, performance, object-cache, page-cache, redis, security-hardening, wp-config, plugins, php, web-development, page-caching, wordpress-hardening]
level: advanced
status: docs-checked
description: "WordPress performance layers (object cache, page cache, transients) and the hardening steps a security audit actually checks."
sources:
  - https://developer.wordpress.org/reference/classes/wp_object_cache/
  - https://developer.wordpress.org/advanced-administration/security/hardening/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WordPress performance and security hardening

**Goal:** the specific layers that make a WordPress site fast under real
traffic, and the hardening checks that stop the most common attack vectors.

## 1. Object cache vs page cache
- **Page cache** (a caching plugin, or a reverse proxy or CDN edge rule):
  caches the full rendered HTML response, skips PHP on a hit. Biggest win for
  anonymous traffic; cached HTML must never be shared between logged-in users,
  so page caches normally bypass logged-in requests.
- **Object cache** (`wp_cache_get`/`wp_cache_set`): by default the object cache
  is non-persistent. Data lives in memory only for the duration of the
  request, so it is not stored across page loads unless you install a
  persistent cache plugin (for example Redis Object Cache, which needs a Redis
  server). A plugin's `wp_cache_set` caching therefore does nothing across
  requests without one. Defining `WP_CACHE` has no effect on this.
- **Transients API:** use it if you need to guarantee data is cached. With a
  persistent object cache it uses the `wp_cache_*` functions; without one it
  caches to the options table. Expired transients are only deleted when
  requested.
```php
$count = get_transient('event_count');
if ($count === false) {
    $count = (new WP_Query(['post_type' => 'event', 'posts_per_page' => -1]))->found_posts;
    set_transient('event_count', $count, HOUR_IN_SECONDS);
}
```
Fetching everything with `posts_per_page => -1` on a large content type is an
unbounded query: paginate or cache the count.

## 2. Hardening checklist
- `wp-config.php`: `define( 'DISALLOW_FILE_EDIT', true );` removes the admin
  theme and plugin file editor.
- Lock file permissions down as far as possible and loosen them only when write
  access is needed; follow the permission scheme in the Hardening WordPress guide.
- Keep core, themes and plugins current, and keep regular, tested backups.

## Verify
- [ ] A persistent object cache backend is actually installed and active, not assumed from plugin claims.
- [ ] `DISALLOW_FILE_EDIT` is set.
- [ ] Core, theme, and all active plugins are confirmed current.

## Checked
2026-11-01. Confirmed against the WP_Object_Cache reference (non-persistent by default, persistent cache plugins, Transients behaviour, WP_CACHE no longer effective) and the Hardening WordPress guide (DISALLOW_FILE_EDIT, file permissions, backups). Removed: query-count figures, Query Monitor, meta_query and autoload claims, XML-RPC, login limiting, exploit-share and database-prefix statements, salts guidance.
Method: documentation only; no commands were run.
