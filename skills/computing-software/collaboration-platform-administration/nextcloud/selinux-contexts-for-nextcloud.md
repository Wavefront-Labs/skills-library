---
id: computing-software.collaboration-platform-administration.nextcloud.selinux-contexts-for-nextcloud
name: selinux-contexts-for-nextcloud
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [selinux, semanage, restorecon, httpd-sys-rw-content-t, httpd-unified]
level: advanced
status: docs-checked
description: "Fix Nextcloud permission denied errors on SELinux with semanage fcontext labels and restorecon, remove labels on uninstall, and handle web updater writes."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/installation/selinux_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let the web server write the paths Nextcloud needs.

Symptom: `permission denied` errors in Nextcloud logs after a new install. SELinux may be the cause even when the audit log shows no denial, because SELinux does not log every system call used to verify access.

For most systems with default distro profiles, run as root, adjusting the paths:

```
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/data(/.*)?'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/config(/.*)?'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/apps(/.*)?'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/.htaccess'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/.user.ini'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/html/nextcloud/3rdparty/aws/aws-sdk-php/src/data/logs(/.*)?'
restorecon -Rv '/var/www/html/nextcloud/'
```

After uninstalling, remove the labels with the same commands using `semanage fcontext -d` instead of `-a -t ...`, then `restorecon -Rv` again.

With customised policies where these examples do not work, the HTTP server needs write access to the `data`, `config` and `apps` directories.

Web updater: to update through the web interface you may need `setsebool httpd_unified on`. After the update disable write access again with `setsebool -P httpd_unified off`.

LDAP: the LDAP backend may need an SELinux setting too, referenced in the LDAP page.

Check: re-trigger the failing action and confirm the permission errors are gone from the Nextcloud log.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/installation/selinux_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
