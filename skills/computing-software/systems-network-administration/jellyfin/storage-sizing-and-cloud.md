---
id: computing-software.systems-network-administration.jellyfin.storage-sizing-and-cloud
name: storage-sizing-and-cloud
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, storage, transcode-cache, rclone, mergerfs, cloud-storage, image-extraction]
level: practitioner
status: docs-checked
description: "Size the database and transcode folder, and use rclone with mergerfs for cloud storage while disabling image extraction."
sources: ["https://jellyfin.org/docs/general/administration/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sizing storage and using cloud providers

**Docker and VMs.** A database for a moderate-sized library can grow from 10 to 100 GB. The transcoding folder typically needs about as much space as the original media at an equivalent bitrate; the docs give a 50 GB Blu-ray remux ending up as roughly 60 GB or as little as 15 GB after transcoding. If the transcode folder shares storage with the database, budget for both so nothing fills the disk.

**Cloud storage.** rclone is a popular way to attach cloud storage to a Jellyfin server and runs on most operating systems. To combine local and cloud filesystems, pair it with a union filesystem such as mergerfs. When using cloud storage, disable image extraction in the library settings, because extracting images requires downloading the entire file.

**mergerfs.** The mergerfs project documents things it should not be used for, so read that list first. The Jellyfin page links a recommended rclone config and a quick guide to examining a mergerfs mount. A union mount is also how real-time monitoring can work over network filesystems that lack inotify (see `computing-software.systems-network-administration.jellyfin.real-time-monitoring-inotify`).

## Checked

2026-11-03. Confirmed against the Jellyfin Storage page: 10 to 100 GB database, transcode folder sizing and 50 GB remux example (~60 GB or ~15 GB), rclone with mergerfs, disable image extraction for cloud. Removed: an unsupported forum attribution and the invented planning check.

Method: documentation only; no commands were run.
