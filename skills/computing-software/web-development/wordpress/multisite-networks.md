---
id: computing-software.web-development.wordpress.multisite-networks
name: multisite-networks
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, multisite, network-admin, switch-to-blog, domain-mapping, wp-cli, php, web-development]
level: practitioner
status: docs-checked
description: "Running WordPress Multisite: subdomain vs subdirectory setup, switch_to_blog pitfalls, domain mapping and WP-CLI site commands."
sources:
  - https://developer.wordpress.org/advanced-administration/multisite/create-network/
  - https://developer.wordpress.org/reference/functions/switch_to_blog/
  - https://developer.wordpress.org/advanced-administration/multisite/domain-mapping/
  - https://developer.wordpress.org/cli/commands/site/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multisite networks

**Goal:** run many sites from one install with plugins that behave correctly per site and per network.

## 1. When to use it
Good for: many similar sites sharing code and users (universities, franchises, intranets). Poor for: unrelated client sites (one bad plugin/load spike affects all, backups/restores are all-or-nothing, harder to move a single site out).

## 2. Setup
```php
// wp-config.php, before "That's all, stop editing!"
define( 'WP_ALLOW_MULTISITE', true );
```
Tools > Network Setup, choose subdomains (`site1.example.com`; wildcard DNS is only needed for on-demand domain-based sites, and the installer's wildcard warning can be ignored if it does not apply) or subdirectories (`example.com/site1`). Then add the generated constants and rewrite rules shown on the Network Setup screen.

## 3. switch_to_blog
```php
foreach ( get_sites( [ 'fields' => 'ids', 'number' => 100 ] ) as $site_id ) {
    switch_to_blog( $site_id );
    $count = wp_count_posts()->publish;
    restore_current_blog();                   // always pair, even on early return
}
```
It sets the blog ID on `$wpdb` and switches the object cache, and does not check that the blog exists (queries against a non-existent site hit non-existent tables). Skipping `restore_current_blog()` after a switch can leave WordPress building wrong URLs; `restore_current_blog()` restores the previous blog, not the original one.

## 4. Domains
Domain mapping is native from WordPress 4.5 (earlier versions need a plugin). Build the network first and confirm subsites can be created before mapping; see the domain-mapping page for the `COOKIE_DOMAIN` setting.

## 5. WP-CLI
```bash
wp site create --slug=newsite
```
See the `wp site` command reference for the full list of subcommands.

## Verify
- [ ] Backups and restores tested for the whole network; procedure exists for extracting a single site.

## Checked
2026-10-31. Confirmed against the WordPress Create A Network, Domain Mapping and switch_to_blog pages and the WP-CLI site reference: WP_ALLOW_MULTISITE, wildcard DNS note, native domain mapping from 4.5, switch_to_blog behaviour and restore_current_blog pairing, wp site create --slug. Removed: one-month subdirectory rule, table layout, plugin activation rules, switch cost and plugin/constant claims, TLS and cookie advice, other WP-CLI examples.
Method: documentation only; no commands were run.
