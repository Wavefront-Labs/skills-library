---
id: computing-software.collaboration-platform-administration.nextcloud.php-modules-required-and-recommended
name: php-modules-required-and-recommended
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [php-modules, pdo-mysql, intl, sodium, php-m]
level: practitioner
status: docs-checked
description: "Prepare PHP for Nextcloud: required modules, one database connector, and recommended intl, sodium, sysvsem, caching and CLI modules, verified with php -m."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/installation/php_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: have a complete PHP before running the installer. Skip this if you use a turnkey method (AIO, Snap, NCP, community Docker), whose PHP is preconfigured.

Required modules: `ctype`, `curl`, `DOM`, `fileinfo`, `filter` (only on Mageia and FreeBSD), `GD`, `xml` (SimpleXML, XMLReader, XMLWriter; needs `libxml2` 2.7.0 or later), `mbstring`, `OpenSSL`, `posix`, `session`, `zip`, `zlib`. Several (`ctype`, `fileinfo`, `OpenSSL`) are normally built in. The xml extension is packaged as `php-xml` or shown as `libxml`.

One database connector: `pdo_mysql` (MySQL or MariaDB), `pdo_pgsql`, or `pdo_sqlite` (3 or later, usually not recommended for performance).

Recommended:
- `intl`: fixes sorting of non-ASCII characters and speeds translation.
- `sodium`: Argon2 hashing, needed on PHP below 8.4 if built without `libargon2`. If missing, bcrypt is used, but accounts hashed with Argon2 (for example after migrating servers) cannot log in.
- `sysvsem`: System V semaphores that coordinate preview generation; previews still work without it.
- Caching: APCu (4.0.6 or later), `redis`/phpredis (2.2.6 or later, required for Transactional File Locking), or `KeyValueCache` to avoid a module.
- CLI: `pcntl` (do not disable `pcntl_signal` and `pcntl_signal_dispatch`), and `phar` for the command line updater.
- Media: `exif`, `imagick`, and ffmpeg/avconv or LibreOffice for previews.

Check a module with:

```
php -m | grep -i <module_name>
```

If the package manager says a module is not found after upgrading PHP, it may already be bundled.

Check: run the check for each required module and confirm output.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/installation/php_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
