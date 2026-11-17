---
id: computing-software.systems-network-administration.syncthing.inotify-watch-limits
name: inotify-watch-limits
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, inotify, filesystem-watcher, linux]
level: practitioner
status: docs-checked
description: "Raise the Linux inotify watch limit when the Syncthing filesystem watcher fails to start."
sources: ["https://docs.syncthing.net/users/faq.html", "https://docs.syncthing.net/users/syncing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# inotify limits on Linux

## Symptom
The log shows: `Failed to start filesystem watcher for folder <label> (<id>): failed to set up inotify handler. Please increase inotify limits`. Linux typically restricts the number of watches per user (usually 8192); with many directories you need to adjust that number.

## Fix
On many distributions the FAQ gives the first command; the second adjusts the limit immediately:

```sh
echo "fs.inotify.max_user_watches=204800" | sudo tee -a /etc/sysctl.conf
echo 204800 | sudo tee /proc/sys/fs/inotify/max_user_watches
```
On Arch Linux and potentially others the FAQ prefers a separate file: the same `fs.inotify.max_user_watches=204800` line written with `sudo tee -a` to `/etc/sysctl.d/90-inotify-max-user-watches.conf`. The persisted setting only takes effect after a reboot, so the second command adjusts the limit immediately.

## If you do not want the watcher
Set the folder's `fsWatcherEnabled` to `false` and rely on full scans (`rescanIntervalS`). The FAQ says Syncthing scans periodically every hour when watching and every minute when the watcher is disabled, and that scanning can cause CPU spikes for large folders. The sync page advises keeping regular full scans even with the watcher enabled.

## Notes
The watcher accumulates changes for 10 s (adjustable with `fsWatcherDelayS`) and deleted files are delayed a further minute, so expect a slight delay before a change appears on another device.

## Checked
2026-11-04. Read the FAQ entry on inotify limits and the scan description, and Understanding Synchronization: error text, 8192 default, both sysctl forms, the immediate command, scan intervals and watcher delays. Removed the claim about negated ignore patterns and extra watches, which neither page states.
Method: documentation only; no commands were run.
