---
id: computing-software.systems-network-administration.linux.grub-timeout-and-hidden-menu
name: grub-timeout-and-hidden-menu
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, grub, grub-timeout, grub-timeout-style, grub-hidden-menu, grub-recordfail, grub-default]
level: intro
status: docs-checked
description: "Control whether the GRUB menu shows: GRUB_TIMEOUT and GRUB_TIMEOUT_STYLE values, how a key press interrupts a hidden or countdown timeout, and regenerating the config."
sources:
  - https://www.gnu.org/software/grub/manual/grub/html_node/Simple-configuration.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# GRUB timeout and hidden menus

## Settings (/etc/default/grub)
| Variable | Effect |
|---|---|
| `GRUB_TIMEOUT=5` | seconds before the default boots (default 5); `-1` waits indefinitely; `0` boots immediately without showing the menu |
| `GRUB_TIMEOUT_STYLE=menu` | always show menu |
| `GRUB_TIMEOUT_STYLE=countdown` | the timeout is counted (with a countdown) before the menu is displayed |
| `GRUB_TIMEOUT_STYLE=hidden` | the timeout is counted silently before the menu is displayed; a key press interrupts it |

Apply by regenerating the configuration with `grub-mkconfig` (many distributions wrap it as `update-grub`).

## Reaching a hidden menu
- During the hidden timeout, pressing **Esc** or **F4**, or holding **Shift**, interrupts it (the GRUB manual describes this for `GRUB_HIDDEN_TIMEOUT`, which is deprecated in favour of `GRUB_TIMEOUT_STYLE`).

## Server recommendation
`GRUB_TIMEOUT=5`, `GRUB_TIMEOUT_STYLE=menu` plus a serial console, so the menu can be reached remotely.

## Gotchas
- Editing the generated `grub.cfg` directly is lost the next time `grub-mkconfig` runs.
- `GRUB_TIMEOUT=0` boots without displaying the menu, so it cannot be interrupted from the menu.

## Verify
- [ ] The regenerated `grub.cfg` reflects the value you set.
- [ ] A reboot on the console/serial shows (or hides) the menu as intended.

## Checked

Documentation check. Checked 2026-10-27 against the GNU GRUB manual source (docs/grub.texi, read from the rhboot/grub2 mirror on 2026-10-27 because gnu.org returned HTTP 429): `GRUB_TIMEOUT` (default 5, `0` boots without displaying the menu, `-1` waits indefinitely), `GRUB_TIMEOUT_STYLE` values `menu`, `countdown` and `hidden` (timeout counted before the menu is shown), Esc, F4 and Shift interrupting the hidden timeout, and `GRUB_HIDDEN_TIMEOUT` being deprecated. Removed `GRUB_RECORDFAIL_TIMEOUT`, `menu_auto_hide`, the BIOS/UEFI key split and the os-prober and cloud-image remarks, which the manual does not cover.
Method: documentation only; no commands were run.
