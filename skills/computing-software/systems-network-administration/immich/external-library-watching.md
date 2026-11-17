---
id: computing-software.systems-network-administration.immich.external-library-watching
name: external-library-watching
category: computing-software
field: systems-network-administration
product: immich
tags: [library-watcher, inotify, periodic-scan, enospc, cron]
level: advanced
status: docs-checked
description: "Keep an Immich external library current: the experimental file watcher, ENOSPC inotify limits, hangs, and the cron-based periodic scan."
sources:
  - https://docs.immich.app/features/libraries
  - https://docs.immich.app/administration/system-settings
  - https://docs.immich.app/install/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick up new files in an external library either instantly or on a schedule.

Automatic watching is experimental and for advanced users. When enabled, Immich imports a file whenever the operating system reports a change, without rescanning. It generally does not work over network drives; use periodic scanning there.

Enable it in System Settings under External Library, or in the config file:

```json
"library": {
  "scan": { "cronExpression": "0 0 * * *", "enabled": true },
  "watch": { "enabled": false }
}
```

Periodic scanning: an automatic scan job runs once a day by default. As admin, set the interval under Administration, Settings, External Library, using a preset or cron format. The nightly job also cleans libraries stuck in deletion; "Scan all libraries" on the library page triggers that cleanup.

If the log shows `ENOSPC: System limit for number of file watchers reached`, raise the inotify limit. The sysctl key is `fs.inotify.max_user_watches`, default 8192; set it above the number of files you will watch. Immich watches all files in the import paths, including ignored ones.

In rare cases the watcher hangs and blocks Immich from starting. Disable the library watcher in the configuration file. If you enabled it from the Immich UI, disable the microservices in the compose file, start Immich, switch the watcher off in the admin settings, stop Immich, re-enable the microservices and start normally.

Deleting a library deletes all its assets immediately and drops the library from the list; the background removal may take a long time.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/libraries in full (Automatic watching, Nightly job, Deleting a Library, Set Custom Scan Interval), administration/system-settings (External Library) and the default `library` block in install/config-file.
Reworded: the watcher-hang recovery steps, to the full sequence on the page.
Method: documentation only; no commands were run.
