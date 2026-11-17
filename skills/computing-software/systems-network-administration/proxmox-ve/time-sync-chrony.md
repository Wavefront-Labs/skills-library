---
id: computing-software.systems-network-administration.proxmox-ve.time-sync-chrony
name: time-sync-chrony
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [ntp, chrony, time-sync, timesyncd, chrony-conf]
level: intro
status: docs-checked
description: "Keep node clocks synchronized with chrony or systemd-timesyncd, which the cluster stack and Ceph depend on."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The cluster stack relies heavily on precisely synchronized time on all nodes, and some other components, such as Ceph, also will not work properly if local time is not in sync. Since Proxmox VE 7 the default NTP daemon is chrony (version 6 used systemd-timesyncd); both are preconfigured with public servers. When upgrading to 7 the docs recommend manually installing chrony, ntp or openntpd.

For nodes behind restrictive firewalls without public internet access, set up local NTP servers and point the daemon at them.

chrony: edit `/etc/chrony/chrony.conf`:

```
server ntp1.example.com iburst
server ntp2.example.com iburst
server ntp3.example.com iburst
```

Then `systemctl restart chronyd` and confirm with `journalctl --since -1h -u chrony`, which should show a line like "Selected source 10.0.0.1 (ntp1.example.com)".

systemd-timesyncd: set `NTP=ntp1.example.com ntp2.example.com` under `[Time]` in `/etc/systemd/timesyncd.conf`, then `systemctl restart systemd-timesyncd` and check `journalctl --since -1h -u systemd-timesyncd` for "Using NTP server".

Check the journal after changing servers to confirm the new ones are in use. Joining a cluster requires date and time to be synchronized (a stated requirement in the cluster chapter), so fix time before running `pvecm add`.

## Checked

Checked 2026-11-08 against the Time Synchronization section of chapter-sysadmin (read in full) and the cluster requirements list in chapter-pvecm (the "Date and time must be synchronized" line only; rest of that chapter not read for this skill). Removed the claims that a wrong server name "fails quietly" and that Ceph "fails" outright (the docs say it will not work properly).

Method: documentation only; no commands were run.
