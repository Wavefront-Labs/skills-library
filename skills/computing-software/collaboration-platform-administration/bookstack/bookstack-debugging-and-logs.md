---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-debugging-and-logs
name: bookstack-debugging-and-logs
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, debugging, app-debug, laravel-log, permissions, white-screen, app-url, update-url]
level: intro
status: docs-checked
description: "Debug BookStack: APP_DEBUG caution, laravel.log location, web server error logs, and fixes for blank pages, missing styles, bad credentials and broken links after a URL change."
sources: ["https://www.bookstackapp.com/docs/admin/debugging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack debugging

`APP_DEBUG=true` in `.env` shows full errors but can expose credentials to visitors: enable it only when nobody else can reach the instance, then turn it off.

Logs: BookStack errors go to `storage/logs/laravel.log` under the install root (on the Ubuntu installer layout `/var/www/bookstack/storage/logs/laravel.log`). Recent entries: `tail -n 400 storage/logs/laravel.log | grep '\[20' -A 3`. If the file is missing, `storage/logs` is probably not writable. A plain unstyled error page comes from the web server, so check its error log (Apache `error.log`, nginx `error.log`).

Common problems:

- Blank white screen: usually permissions; run `chown -R www-data:www-data bootstrap/cache storage public/uploads` from the install folder, else check web server logs.
- No styles and huge icons: `APP_URL` must match the access URL including http or https, and you should be on the `release` branch.
- Database or auth credential failures: quote `.env` passwords with special characters, e.g. `DB_PASSWORD="hunter#2@"`.
- Dynamic UI broken: check `APP_URL`, disable Cloudflare Rocket Loader, review the Custom HTML Head setting, read the browser console.
- Broken links or images after changing `APP_URL`: back up, then `php artisan bookstack:update-url <old> <new>`.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/debugging/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
