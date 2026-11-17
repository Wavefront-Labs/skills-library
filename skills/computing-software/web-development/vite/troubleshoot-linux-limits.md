---
id: computing-software.web-development.vite.troubleshoot-linux-limits
name: troubleshoot-linux-limits
category: computing-software
field: web-development
product: vite
tags: [stalled-requests, enospc-watchers, inotify-limits, file-descriptor-limit]
level: advanced
status: docs-checked
description: "Fix stalled Vite requests and ENOSPC watcher errors on Linux: raise ulimit and inotify sysctl limits, ignore big directories, or switch to polling."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requests stalled forever (Linux): Vite serves many unbundled files, which can exceed file descriptor and inotify limits.

```shell
ulimit -Sn            # check
ulimit -Sn 10000      # temporary; the hard limit may need changing; restart the browser
sysctl fs.inotify
sudo sysctl fs.inotify.max_queued_events=16384
sudo sysctl fs.inotify.max_user_instances=8192
sudo sysctl fs.inotify.max_user_watches=524288
```

If that fails, set `DefaultLimitNOFILE=65536` (uncommented) in `/etc/systemd/system.conf` and `/etc/systemd/user.conf`; on Ubuntu add `* - nofile 65536` to `/etc/security/limits.conf` instead. These persist but need a restart. A VS Code devcontainer can also look stalled (see port forwarding).

`ENOSPC: System limit for number of file watchers reached`: too many files for the default limit (roughly 8,192-10,000). Raise `fs.inotify.max_user_watches` (persist it in `/etc/sysctl.conf`, then `sudo sysctl -p`), exclude big directories with `server.watch.ignored`, or use `server.watch.usePolling` (more CPU).

## Checked

2026-11-04. Confirmed against the Vite troubleshooting guide (docs/guide/troubleshooting.md, Dev Server): ulimit and fs.inotify values, DefaultLimitNOFILE files, Ubuntu limits.conf line, restart requirement, ENOSPC remedies. Nothing removed.

Method: documentation only; no commands were run.
