---
id: computing-software.systems-network-administration.linux.scheduled-shutdown-and-firmware-reboot
name: scheduled-shutdown-and-firmware-reboot
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, shutdown-schedule, firmware-setup, shutdown-command, wall, systemctl-reboot, nologin]
level: intro
status: docs-checked
description: "Schedule, announce and cancel shutdowns and reboots (shutdown +N, -c, wall), reboot straight into UEFI setup or a specific boot entry, and block logins before maintenance."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/shutdown.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
  - https://man7.org/linux/man-pages/man8/pam_nologin.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled shutdown and firmware reboot

## Schedule and announce
```bash
shutdown -r +15 "Kernel update: rebooting in 15 minutes, save your work"
shutdown -h 23:30 "Power maintenance"
shutdown -c "Reboot cancelled"          # cancel (also broadcasts)
wall "Maintenance at 02:00 UTC"          # broadcast to all terminals
```
5 minutes before the time, systemd-logind creates `/run/nologin` — non-root logins are refused (pam_nologin).
Create it yourself to block logins earlier: `echo "Maintenance in progress" > /run/nologin`.

## Immediate actions
`systemctl reboot`, `systemctl poweroff`, `systemctl halt`, `systemctl soft-reboot` (userspace only, systemd 254+).
Inhibitors (`systemd-inhibit --list`) can delay; `-i` is a shortcut for `--check-inhibitors=no`.

## Firmware and boot-entry targeting
```bash
systemctl reboot --firmware-setup                      # into the firmware setup interface (not available on all systems)
systemctl reboot --boot-loader-entry=<id>               # only boot loaders that support it
systemctl reboot --boot-loader-menu=30                 # show the boot loader menu with a 30 s timeout
efibootmgr -n 0003 && reboot                           # one-time UEFI BootNext
```

## Gotchas
- `systemctl reboot -ff` executes the reboot immediately without contacting the service manager; last resort only.
- `--firmware-setup` and `--boot-loader-menu=` depend on firmware and boot loader support.

## Verify
- [ ] `shutdown` broadcast seen by logged-in users; scheduled time visible via logind; `/run/nologin` appears 5 minutes before.

## Checked

Checked 2026-10-27 against systemd man pages (shutdown, systemctl, systemd-inhibit, udev, udevadm, sd-login, systemd.resource-control), linux-pam pam_nologin and pam_motd sources, efibootmgr man page source, current main, 2026-10-27. Confirmed: shutdown +m and hh:mm syntax, -c, wall message, /run/nologin created 5 minutes before, pam_nologin purpose, systemctl reboot/poweroff/halt, soft-reboot since systemd 254, -i, -ff, --firmware-setup, --boot-loader-entry and --boot-loader-menu, efibootmgr -n for BootNext, systemd-inhibit --list. Removed or softened: logind busctl property, GRUB grub-reboot example (gnu.org documentation is not readable), cloud billing remark, firmware error message.

Method: documentation only; no commands were run.
