---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-manual-installation
name: bookstack-manual-installation
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, installation, php, composer, laravel, artisan, mariadb, mysql, web-root]
level: practitioner
status: docs-checked
description: "Install BookStack manually: PHP, extension, database and Composer requirements, clone the release branch, .env, writable folders, key generate, migrate, and the default login."
sources: ["https://www.bookstackapp.com/docs/admin/installation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack manual installation

Requirements: PHP 8.2+ with extensions curl, dom, gd, iconv, mbstring, mysqlnd, openssl, pdo, pdo_mysql, tokenizer, xml, zip (optional: ldap for LDAP auth, exif for image rotation); MySQL 8.0+ or MariaDB 10.6+ (one database, with all permissions since the app manages the schema); Git; Composer 2.2+; a PHP-capable web server. Shared hosting is unsupported.

Steps:

```
git clone https://source.bookstackapp.com/bookstack.git --branch release --single-branch bookstack
cd bookstack
composer install --no-dev
cp .env.example .env     # then set database and mail details
php artisan key:generate
php artisan migrate
```

Make `storage`, `bootstrap/cache` and `public/uploads` writable by the web server. Point the web root (nginx `root`, Apache `DocumentRoot`) at the `public` folder; without Apache `.htaccess` you need your own URL rewrite rules. Default login is `admin@admin.com` / `password`: change both at once.

Alternatives: community Docker images (LinuxServer.io, solidnerd), or the project's Ubuntu 22.04/24.04/26.04 install scripts for fresh OS installs only (they install Apache, MySQL and PHP, can overwrite an existing web setup, do not configure mail or security, and the 26.04 script generates a random admin password shown at the end). Locked out? `php artisan bookstack:create-admin`.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/installation/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: the PHP-patching warning and the rewrite-rule detail, which the page does not state.
Method: documentation only; no commands were run.
