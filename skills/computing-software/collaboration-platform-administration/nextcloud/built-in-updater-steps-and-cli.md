---
id: computing-software.collaboration-platform-administration.nextcloud.built-in-updater-steps-and-cli
name: built-in-updater-steps-and-cli
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [updater, updater-phar, occ-upgrade, maintenance-mode, downgrade]
level: practitioner
status: docs-checked
description: "Run the Nextcloud built-in updater from the command line, know what each step does, why backups come first, and that downgrading is unsupported."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/maintenance/update.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: update the code safely, then migrate.

Warnings from the docs: downgrading is unsupported and risks corrupting data. To revert, install the older version fresh and restore from backup. The updater does not back up your database or data directory, so take your own backup before every update.

Command line run, as the web server user, from the install:

```
sudo -E -u www-data php /var/www/nextcloud/updater/updater.phar
```

Check the displayed information and answer Y. An update-notification banner and admin Version section lead to the web updater.

Steps it performs:
1. checks only expected files exist
2. checks write permissions
3. enables maintenance mode
4. backs up the code (not data or database) to `updater-INSTANCEID/backups/nextcloud-CURRENTVERSION/` in the data directory
5. downloads the new version to `updater-INSTANCEID/downloads/`, then extracts it
6. replaces entry points such as `index.php`, `remote.php` and `ocs/v1.php` with dummy files so clients get a proper maintenance response
7. deletes old files, except data, config, non-shipped apps and themes
8. moves new files into place
9. web mode only: asks whether to keep maintenance mode, which lets you run `occ upgrade` yourself

The updater only replaces files. The migration phase upgrades the database and apps; in command line mode the updater offers to run `occ upgrade` for you.

Check: after migration, maintenance mode is off and the admin overview shows the new version.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/maintenance/update.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
