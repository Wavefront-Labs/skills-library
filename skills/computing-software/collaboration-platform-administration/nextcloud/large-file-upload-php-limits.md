---
id: computing-software.collaboration-platform-administration.nextcloud.large-file-upload-php-limits
name: large-file-upload-php-limits
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [upload-max-filesize, post-max-size, user-ini, php-timeouts, temp-space]
level: practitioner
status: docs-checked
description: "Raise Nextcloud uploads above 512MB with upload_max_filesize and post_max_size in php.ini or .user.ini, size temp space, and handle timeouts."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/big_file_upload_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: allow uploads larger than the default 512MB.

Default maximum upload is 512MB; raise it up to what your filesystem and OS allow. Hard limits: under 2GB on 32-bit, under 2GB with IE6 to IE8, under 4GB with IE9 to IE11. The sync client is not affected, as it uploads in smaller chunks.

System side:
- Use the latest PHP.
- Disabling user quotas makes them unlimited.
- Temp space must hold parallel uploads. With a 10GB maximum and 100 simultaneous uploaders, you need at least 10x100 GB.

PHP side. Set in the right php.ini (find it under *Loaded Configuration File* in `phpinfo`):

```
php_value upload_max_filesize 16G
php_value post_max_size 16G
php_value max_input_time 3600
php_value max_execution_time 3600
```

Nextcloud ships its own `.htaccess`, but `php-fpm` cannot read PHP settings from it, so with `php-fpm` put the values in `nextcloud/.user.ini` instead.

The two size settings may not apply to single-file WebDAV `PUT` or chunked uploads. For those, PHP and web server timeouts limit upload size. If logs show PHP timeouts, raise the timeout values (in seconds).

Web server limits can also block large uploads. For Apache check `LimitRequestBody`, `SSLRenegBufferSize`, `Timeout`, and for `mod_fcgid` `FcgidMaxRequestInMem`. `mod_reqtimeout` can stop long uploads: disable it or raise `RequestReadTimeout`.

Check: upload a file just over the old limit and watch for timeouts in the logs.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/big_file_upload_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
