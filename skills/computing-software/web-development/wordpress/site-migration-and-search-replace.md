---
id: computing-software.web-development.wordpress.site-migration-and-search-replace
name: site-migration-and-search-replace
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, wordpress-migration, search-replace, wp-cli, serialized-data, site-url, php, web-development]
level: practitioner
status: docs-checked
description: "Migrating WordPress between hosts or domains: database export/import, serialisation-safe search-replace with WP-CLI, files, URLs and constants, and post-migration checks."
sources:
  - https://developer.wordpress.org/cli/commands/search-replace/
  - https://developer.wordpress.org/advanced-administration/upgrade/migrating/
  - https://developer.wordpress.org/cli/commands/db/export/
  - https://developer.wordpress.org/advanced-administration/server/wordpress-in-directory/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site migration and search-replace

**Goal:** move a WordPress site to a new host and/or domain with no broken URLs, serialised data intact and minimal downtime.

## 1. Inventory
WordPress = database + `wp-content/` (uploads, themes, plugins) + `wp-config.php` (constants, salts, table prefix) + server config (.htaccess/nginx rules, PHP version, cron). Note the PHP and MySQL versions and the table prefix.

## 2. Export and copy
```bash
# source
wp db export --add-drop-table site.sql
# copy wp-content (uploads, themes, plugins) to the new host
```

## 3. Import and replace URLs
```bash
# target (wp-config.php already pointing at the new DB, same $table_prefix)
wp db import site.sql
wp search-replace 'https://old.example.com' 'https://new.example.com' --all-tables-with-prefix --precise --report-changed-only --dry-run
wp search-replace 'https://old.example.com' 'https://new.example.com' --all-tables-with-prefix --precise
wp search-replace 'old.example.com' 'new.example.com' --all-tables-with-prefix --dry-run    # protocol-less leftovers, review first
wp cache flush && wp rewrite flush
```
Prefer `wp search-replace` over raw SQL or sed on the dump: it uses SQL for plain columns but automatically switches to PHP for columns holding serialised data, and `--precise` forces PHP for every column (slower, more reliable for complex serialised data). Use `--skip-columns=guid` as in the command reference's examples.
Multisite: add `--network` and include `wp_blogs` and `wp_site` as in the reference example.

## 4. Config and environment
- `WP_HOME`/`WP_SITEURL` constants override the DB values - check `wp-config.php`.
- Recreate server rules (permalinks, redirects, security headers), cron, object cache config and file permissions.

## 5. Cutover
Freeze content (maintenance mode or editorial freeze), final delta sync of DB + uploads, lower DNS TTL beforehand, switch DNS, issue TLS, keep the old server read-only for a few days. Add 301 redirects old domain -> new for domain changes and update Search Console.

## 6. Check
Re-run `wp search-replace` with `--dry-run` for the old domain and confirm nothing unexpected remains. Crawl the site for 404s and mixed content.

## Verify
- [ ] A `--dry-run` search-replace for the old domain finds nothing unexpected.
- [ ] Widgets, menus, page-builder layouts and media render correctly.
- [ ] Forms, emails (SMTP), cron and logins work on the new host.

## Checked
2026-10-31. Confirmed against the WP-CLI search-replace and db export references: --all-tables-with-prefix, --precise, --report-changed-only, --dry-run, --skip-columns=guid, --network with wp_blogs/wp_site, SQL-to-PHP switch for serialised columns, db export --add-drop-table. Removed: tar and rsync commands, serialisation length example, shuffle-salts, DISABLE_WP_CRON, file permission modes, wp db search, wget crawl, DOMAIN_CURRENT_SITE.
Method: documentation only; no commands were run.
