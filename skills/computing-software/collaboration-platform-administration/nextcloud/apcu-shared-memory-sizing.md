---
id: computing-software.collaboration-platform-administration.nextcloud.apcu-shared-memory-sizing
name: apcu-shared-memory-sizing
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [apcu, apc-shm-size, php-ini, local-cache, serverinfo]
level: advanced
status: docs-checked
description: "Install APCu for Nextcloud, raise apc.shm_size above the 32M default, and monitor the cache so resets do not cause slowdowns."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give the local cache enough memory that it does not keep clearing.

Install the extension:
- Red Hat, CentOS, Fedora: `php-pecl-apcu`
- Debian, Ubuntu, Mint: `php-apcu`

Restart the web server, then add to `config.php`:

```
'memcache.local' => '\OC\Memcache\APCu',
```

Refresh the admin page and the cache warning should disappear. APCu 4.0.6 or newer is required.

Sizing. The default `apc.shm_size` in `php.ini` is 32M, which is usually too low for Nextcloud. The docs suggest 128M as a starting point, and more with many users or many installed apps. That memory must exist on the host, so count it when sizing the number of PHP workers.

Why it matters: a frequently resetting cache causes unexpected slowdowns while it is cleared and refilled.

Monitoring. An admin check tries to detect an undersized cache, but also watch the cache status yourself. Two options are the script that APCu provides and the `serverinfo` app in Nextcloud, which can show APCu cache status.

If the web server runs PHP through several pools or processes, remember the CLI is a separate process (see `occ` runs with its own PHP settings); check what your `phpinfo` shows for the web SAPI.

Check: the cache status shows free memory remaining under normal load, with a low restart count.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/caching_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
