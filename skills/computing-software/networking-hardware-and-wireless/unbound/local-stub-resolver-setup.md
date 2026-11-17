---
id: computing-software.networking-hardware-and-wireless.unbound.local-stub-resolver-setup
name: local-stub-resolver-setup
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, local-stub, systemd-resolved, resolv-conf, macos, persistence]
level: practitioner
status: draft
description: "Make one machine use its own Unbound as the system resolver on Ubuntu (systemd-resolved) or macOS, and keep it running across reboots."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/use-cases/local-stub.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# local stub resolver setup
Prerequisites: Unbound installed, DNSSEC enabled, `interface: 127.0.0.1`, and verified running before changing system DNS, otherwise the connection can break.

Ubuntu (systemd-resolved): in `/etc/systemd/resolved.conf` or `/etc/systemd/resolved.conf.d/unbound.conf` set under `[Resolve]`:
```
DNS=127.0.0.1
DNSSEC=yes
DNSStubListener=no
```
Then `ln -fs /run/systemd/resolve/resolv.conf /etc/resolv.conf` (skip on Ubuntu 24.04, where the link exists) and `systemctl restart systemd-resolved`. Verify that `dig example.com` shows `SERVER: 127.0.0.1#53`. If `unbound-resolvconf` reports "Failed to set DNS configuration" while dig works, `systemctl disable unbound-resolvconf.service`.

Persistence on Ubuntu: package install, `systemctl start unbound.service` and `systemctl enable unbound.service`. Compiled install: create a systemd unit running `/usr/local/sbin/unbound -d -p $DAEMON_OPTS`, then `daemon-reload`, `enable`, `start`.

macOS (Big Sur and later): check with `scutil --dns`, add `127.0.0.1` under Network, Advanced, DNS. Persist with `sudo brew services start unbound` or a LaunchDaemon plist with `KeepAlive` and `RunAtLoad`.
