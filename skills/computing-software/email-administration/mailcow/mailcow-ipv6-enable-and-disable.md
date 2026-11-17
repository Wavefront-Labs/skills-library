---
id: computing-software.email-administration.mailcow.mailcow-ipv6-enable-and-disable
name: mailcow-ipv6-enable-and-disable
category: computing-software
field: email-administration
product: mailcow
tags: [ipv6, enable-ipv6, docker-daemon-ipv6, open-relay, sysctl]
level: advanced
status: docs-checked
description: "Turn IPv6 on or off for the mailcow Docker network with ENABLE_IPV6 and clean up daemon and kernel settings to avoid errors or an open relay."
sources: ["https://docs.mailcow.email/post_installation/firststeps-disable_ipv6/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Managing IPv6 in mailcow

From the 2025-09 update, IPv6 is managed with `ENABLE_IPV6` in `mailcow.conf`. It defaults to `true` when the host supports IPv6. Set `ENABLE_IPV6=false` and restart the whole stack with `docker compose down` then `docker compose up -d`; the mailcow Docker network is recreated from the setting. All services listen on IPv4 and IPv6 when enabled, and only on IPv4 if the container network has just IPv4. The update script also has a helper that adjusts the Docker daemon's IPv6 settings for your host using `jq` and tells you what is still missing in `daemon.json`.

If IPv6 was enabled earlier and you now disable it, also clean up manually. Check `sysctl net.ipv6.conf.all.disable_ipv6 net.ipv6.conf.default.disable_ipv6`. To persist disabling, put `net.ipv6.conf.all.disable_ipv6 = 1`, the same for `default` and `lo`, in `/etc/sysctl.d/99-disable-ipv6.conf` and run `sysctl --system`. In `/etc/docker/daemon.json` remove `"ipv6": true` and `fixed-cidr-v6`, or set `"ipv6": false`, restart Docker and recreate the mailcow stack.

Warning from the docs: if the host has IPv6 and the Docker daemon is not configured correctly, Docker NATs external IPv6 addresses to internal IPv4 ones and they may be treated as internal, which can lead to an open relay. Keep the daemon configuration matching your IPv6 setup.

## Checked

2026-11-04. Confirmed on the Disable IPv6 page (2025-09 and later section): ENABLE_IPV6 default true when the host supports IPv6, full-stack restart recreating the Docker network, the update-script daemon.json helper using jq, listening behaviour, the sysctl check and persistent file, the daemon.json entries to remove, and the open relay warning. The pre-2025-09 procedure is not covered by this skill.

Method: documentation only; no commands were run.
