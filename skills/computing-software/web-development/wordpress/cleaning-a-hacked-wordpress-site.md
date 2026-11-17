---
id: computing-software.web-development.wordpress.cleaning-a-hacked-wordpress-site
name: cleaning-a-hacked-wordpress-site
category: computing-software
field: web-development
product: wordpress
tags: [wordpress-malware-cleanup, hacked-site-recovery, wp-cli-verify-checksums, backdoor-removal, wordpress-security, wordpress]
level: advanced
status: docs-checked
description: "Recovering a hacked WordPress site: containment, forensic backup, checksum checks, finding backdoors and rogue users/options/cron, credential rotation, root cause."
sources:
  - https://developer.wordpress.org/advanced-administration/security/hardening/
  - https://developer.wordpress.org/cli/commands/core/verify-checksums/
  - https://wordpress.org/documentation/article/faq-my-site-was-hacked/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cleaning a hacked WordPress site

## 1. Contain and preserve
- Put the site in maintenance mode or block traffic at the host/WAF; tell the client/stakeholders.
- Take a full copy (files + DB dump) **before** changing anything, for forensics. Save web server access logs.

## 2. Verify and replace code
```bash
wp core verify-checksums                    # modified/extra core files
wp plugin verify-checksums --all            # wordpress.org plugins only
wp core download --force --skip-content     # replace core files
wp plugin install <slug> --force            # reinstall each plugin/theme from official sources
```
Premium plugins/themes: reinstall from the vendor's fresh download. Delete anything unused.

## 3. Hunt persistence
```bash
find wp-content/uploads -type f -name "*.php"                       # PHP files in uploads are suspect
find . -type f -name "*.php" -mtime -14 | sort                       # recently modified
grep -rlE "eval\(|base64_decode\(|gzinflate\(|str_rot13\(|assert\(\$_|preg_replace\(.*/e" wp-content
ls wp-content/mu-plugins                                             # review must-use plugins
```
Database and config:
- `wp user list --role=administrator` and remove unknown admins.
- Check options, widget content and posts for injected `<script>` or spam links (`wp db search "<script" --all-tables`).
- `wp cron event list` for unfamiliar hooks; `.htaccess`/nginx rules for redirects; `wp-config.php` for added includes.

## 4. Rotate everything
- `wp config shuffle-salts`, a forced password reset for all users (especially administrators), the database user password (update `wp-config.php`), SFTP/SSH keys, hosting panel, API keys stored in options/plugins. Change passwords again once the site is confirmed clean.
- Revoke application passwords (`wp user application-password list <user>`).

## 5. Root cause and hardening
Find the entry point (vulnerable plugin version in logs, weak admin password, compromised hosting account, nulled theme) and fix it, or reinfection follows. Then: update everything, `DISALLOW_FILE_EDIT`, least-privilege file permissions and regular tested backups, per the WordPress hardening guide.

## 6. After
Use Google Search Console if the site was flagged; keep monitoring logs for weeks.

## Verify
- [ ] Checksums clean, no PHP in uploads, no unknown admins or cron hooks, all credentials rotated, and the root-cause vulnerability is patched.

## Checked
2026-11-01. Confirmed against the WP-CLI command pages (core download --force/--skip-content, plugin verify-checksums --all, plugin install --force, db search --all-tables, user list --role, config shuffle-salts, cron event list, user application-password list), the Hardening WordPress guide (DISALLOW_FILE_EDIT, permissions, backups) and the My Site Was Hacked FAQ (forced password reset, database password, change passwords again). Removed: wp_usermeta, siteurl and active_plugins checks, session-logout claim, WAF/2FA/integrity monitoring, Search Console menu name.
Method: documentation only; no commands were run.
