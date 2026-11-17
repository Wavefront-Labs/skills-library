---
id: computing-software.systems-network-administration.patch-management.snap-and-flatpak-refresh-control
name: snap-and-flatpak-refresh-control
category: computing-software
field: systems-network-administration
product: patch-management
tags: [snap-refresh, flatpak, third-party-patching, linux-patching, snapd, ubuntu]
level: practitioner
status: gated
description: "Control updates of snap and Flatpak applications on managed Linux: refresh timers, holds, metered settings, enterprise proxies, Flatpak update automation and inventory."
sources:
  - https://snapcraft.io/docs/managing-updates
  - https://github.com/canonical/snapd
  - https://docs.flatpak.org/en/latest/flatpak-command-reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snap and Flatpak refresh control

Snaps and Flatpaks update outside apt/dnf; package-manager patching and many scanners miss
them. Firefox, Chromium, LXD, microk8s and many desktop apps ship this way on Ubuntu.

## Snap
Snaps refresh automatically (default frequency (gated: unconfirmed, source is paywalled or blocked)).
```sh
snap list                                  # versions, revisions, channels
snap refresh --list                        # pending updates
snap refresh                               # update now
snap refresh --time                        # current schedule
snap set system refresh.timer=mon,02:00-04:00      # maintenance window
snap refresh --hold=72h firefox            # postpone one snap (minimum snapd version (gated: unconfirmed, source is paywalled or blocked))
snap refresh --unhold firefox
snap set system refresh.metered=hold       # don't refresh on metered links
```
Fleet: set `refresh.timer`, `refresh.metered` and holds from config management. Landscape snap management and the Snap Store Proxy for air-gapped control (gated: unconfirmed, source is paywalled or blocked).
Revert a bad update: `snap revert firefox` (`snap revert` availability and its use of retained revisions (gated: unconfirmed, source is paywalled or blocked)). `refresh.retain` accepts a number from 2 to 20 per snapd source.

## Flatpak
Updates are applied when someone runs `flatpak update`; desktop software centres may do it per user.
```sh
flatpak list --app --columns=application,version,origin,installation
flatpak remote-ls --updates
flatpak update -y --noninteractive
flatpak update --system -y        # system-wide installs
flatpak mask org.example.App      # mask out updates and automatic installation
```
Automate with a systemd timer:
```ini
# /etc/systemd/system/flatpak-update.service
[Service]
Type=oneshot
ExecStart=/usr/bin/flatpak update -y --noninteractive --system
```
plus a `.timer` with `OnCalendar=daily`.

## Inventory and vulnerability coverage
Collect `snap list` and `flatpak list` into inventory; scanners that only read apt/dnf databases miss them, and a snap is fixed by installing a newer revision, not through apt.

## Gotchas
- Snap auto-refresh can restart services (LXD) mid-day: set timers on servers.
- Holding indefinitely recreates the patching gap: holds need an expiry and a ticket.

## Verify
`snap refresh --list` and `flatpak remote-ls --updates` empty on sampled hosts after the
window; inventory shows current revisions.

## Checked

Checked 2026-10-27 against the snapd source (refresh configuration validation) and the Flatpak command reference; the snapcraft.io documentation could not be read as plain text.
- snapd config keys `refresh.timer`, `refresh.metered` (only value `hold`), `refresh.hold` (RFC 3339 timestamp), `refresh.retain` (2 to 20): confirmed in snapd source.
- Flatpak `update`, `remote-ls`, `list --columns`, `--noninteractive`, `mask` ("mask out updates and automatic installation"): confirmed.
- Claims marked gated above could not be confirmed from readable documentation; the skill therefore stays gated.
Method: documentation only; no commands were run.
