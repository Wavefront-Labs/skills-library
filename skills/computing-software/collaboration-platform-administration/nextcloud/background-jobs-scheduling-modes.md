---
id: computing-software.collaboration-platform-administration.nextcloud.background-jobs-scheduling-modes
name: background-jobs-scheduling-modes
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [background-jobs, cron, ajax, webcron, cron-php]
level: practitioner
status: docs-checked
description: "Choose between AJAX, Webcron and system cron for Nextcloud background jobs, and know why only cron suits multi-user servers or external storage."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/background_jobs_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the scheduler that runs `cron.php` reliably.

Nextcloud apps register housekeeping with `cron.php` automatically, such as garbage collecting temporary files or rescanning external file systems.

The three modes:
- AJAX (default): one background job runs each time a user visits a page. Least reliable, needs regular visits. Fine only for a single-user instance.
- Webcron: an external service calls `cron.php` over HTTP(S). Only one job runs per call, because the web server limits resources. Called every 5 minutes that is 288 jobs a day, so use it only for very small instances (1 to 5 users).
- Cron: the operating system runs `cron.php`. This is the recommended method and avoids web server limits.

The docs say to move to cron when you use the Activity app or external storage, or when multiple users share the server.

Crontab for the web server user (often `www-data` or `wwwrun`), every 5 minutes:

```
crontab -u www-data -e
*/5  *  *  *  * php -f /var/www/nextcloud/cron.php
```

Replace the path with your install path. Some systems need `php-cli` instead of `php`. List the result with `crontab -u www-data -l`.

Check: once `cron.php` has run from the command line or cron service, the admin background-jobs setting switches to Cron by itself; selecting it manually is not mandatory.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/background_jobs_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
