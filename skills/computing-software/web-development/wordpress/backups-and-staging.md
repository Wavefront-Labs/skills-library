---
id: computing-software.web-development.wordpress.backups-and-staging
name: backups-and-staging
category: computing-software
field: web-development
product: wordpress
tags: [wordpress, wordpress-backups, staging, restore-testing, wp-cli, disaster-recovery, php, web-development, staging-site]
level: practitioner
status: docs-checked
description: "Backing up WordPress and running staging: what to back up, scheduled DB and file backups off-site, restore drills, staging sync rules and avoiding staging side effects."
sources:
  - https://developer.wordpress.org/advanced-administration/security/backup/
  - https://developer.wordpress.org/cli/commands/db/export/
  - https://restic.readthedocs.io/en/stable/
  - https://make.wordpress.org/core/2020/07/24/new-wp_get_environment_type-function-in-wordpress-5-5/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Backups and staging

**Goal:** recover any site to a recent point in under an hour, and test changes on staging without emailing customers or charging cards.

## 1. What to back up
- Database (all content, settings, users, orders).
- `wp-content/uploads` (irreplaceable media).
- `wp-config.php` and server config.
- Themes/plugins: reinstallable from version control or wordpress.org, but back up custom/premium code that isn't in git.

## 2. Schedule and store
```bash
# nightly DB (plus hourly for busy e-commerce), compressed, encrypted, off-site
wp db export - --single-transaction --quick | gzip | age -r "$BACKUP_PUBKEY" > /backups/db-$(date +%F-%H%M).sql.gz.age
restic -r s3:s3.<REGION>.amazonaws.com/acme-backups backup /var/www/site/wp-content/uploads /backups
restic forget --keep-hourly 24 --keep-daily 14 --keep-weekly 8 --keep-monthly 12 --prune
```
Principles: keep copies in different locations (the WordPress backup handbook suggests e.g. the hosting server plus cloud storage), stored outside the site's own account so a compromised server can't delete them, encrypted, with retention long enough to predate a slow-detected hack. Backup plugins work when shell access isn't available; host snapshots are a supplement, not a substitute.

## 3. Restore drills
A backup you haven't restored is a guess. Quarterly: restore DB + uploads to a scratch environment, run `wp search-replace` for its URL, log in, check recent orders/posts. Time it - that's your real RTO.

## 4. Staging
- Clone production (DB + uploads) to `staging.example.com`, replace URLs with WP-CLI search-replace.
- `define( 'WP_ENVIRONMENT_TYPE', 'staging' );` and act on it: disable outgoing mail, switch payment gateways to test mode, disable analytics and marketing integrations, and keep search engines out (HTTP auth).
- Code moves **up** via git/CI deploys; content moves **down** (prod -> staging). Never push a staging DB over production on a live site with new orders/comments - merge content changes manually or with tooling built for it.
- Mask personal data in staging copies where possible (`wp db query` scripts to anonymise users/orders).

## 5. Before risky changes
Take an on-demand backup before core/plugin updates, and test updates on staging first for business-critical plugins (WooCommerce, page builders, membership).

## Verify
- [ ] Last successful backup is < 24h old and alerts fire on failure.
- [ ] A restore drill in the last quarter succeeded within the target time.
- [ ] Staging sends no real emails/payments and is protected by an auth prompt.

## Checked

2026-11-02. Checked against the WordPress backup handbook page (back up database and files; keep copies in different locations), the WP-CLI db export page (file name - writes to STDOUT; extra flags pass through to mysqldump), the wp_get_environment_type announcement (values local, development, staging, production; WP_ENVIRONMENT_TYPE) and the restic documentation (forget --keep-hourly/daily/weekly/monthly and --prune; S3 repository URL form s3:s3.<region>.amazonaws.com/bucket). Corrected the S3 repository URL to the documented regional form. Removed: the 3-2-1 rule wording (the handbook only says copies in different locations), the named backup plugins, Mailpit, the blog_public setting and the noindex check, none of which a fetched page states.

Method: documentation only; no commands were run.
