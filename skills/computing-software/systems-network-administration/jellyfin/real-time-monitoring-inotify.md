---
id: computing-software.systems-network-administration.jellyfin.real-time-monitoring-inotify
name: real-time-monitoring-inotify
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, real-time-monitoring, inotify, max-user-watches, sysctl, mergerfs]
level: practitioner
status: docs-checked
description: "Fix real-time library monitoring on Linux: unsupported filesystems and the inotify watch limit error."
sources: ["https://jellyfin.org/docs/general/administration/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Real-time monitoring and inotify limits

Real-time monitoring lets Jellyfin update libraries automatically when files are added or modified. It works only on certain filesystems. On Linux it uses inotify. NFS and rclone mounts do not support inotify; a union filesystem such as mergerfs layered over the network filesystem can provide it.

**Watch limit error.** Large libraries can hit the kernel limit and log:

```log
Error in Directory watcher for: "/media/movies"  System.IO.IOException: The configured user limit (8192) on the number of inotify watches has been reached.
```

Raise the limit. On Debian, Red Hat and similar:

```sh
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.d/40-max-user-watches.conf && sudo sysctl -p
```

On Arch Linux:

```sh
echo fs.inotify.max_user_watches=524288 | sudo tee /etc/sysctl.d/40-max-user-watches.conf && sudo sysctl --system
```

For Docker, apply the change on the host, not in the container.

## Checked

2026-11-03. Confirmed against the Jellyfin Troubleshooting page, Real Time Monitoring section: inotify, NFS/rclone limitation and mergerfs workaround, the 8192 error text, both sysctl commands, Docker host note. Removed: unsupported fallback advice and the invented self-check.

Method: documentation only; no commands were run.
