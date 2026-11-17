---
id: computing-software.systems-network-administration.linux.keyboard-layout-vconsole-xkb
name: keyboard-layout-vconsole-xkb
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, keyboard-layout, vconsole, xkb, localectl, keymap, vconsole-conf, console-font, setfont, loadkeys, initramfs, localisation, sysadmin]
level: intro
status: docs-checked
description: "Set keyboard layouts for the Linux console and X11/Wayland with localectl: vconsole keymaps vs XKB layouts, console fonts, the initramfs LUKS prompt layout, and Debian's keyboard-configuration."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/localectl.html
  - https://www.freedesktop.org/software/systemd/man/latest/vconsole.conf.html
  - https://manpages.debian.org/trixie/keyboard-configuration/keyboard.5.en.html
  - https://manpages.debian.org/trixie/console-setup/console-setup.5.en.html
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.cmdline.7.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyboard layout: vconsole and XKB

**Goal:** the right layout everywhere you type — text console, LUKS passphrase prompt at
boot, and graphical sessions — so passwords work at 3 a.m. on a KVM console.

## 1. Two separate layers
- **Virtual console** (text TTYs, emergency shell, initramfs): keymap names like `uk`, `de-latin1`, `us`.
  Config: `/etc/vconsole.conf` (`KEYMAP=`, `FONT=`).
- **XKB** (X11, most Wayland compositors, GDM): layout/model/variant/options like `gb`, `pc105`, `dvorak`, `ctrl:nocaps`.
  Config: written by `localectl set-x11-keymap`.

## 2. localectl
```bash
localectl status
localectl list-keymaps | grep -i uk
localectl set-keymap uk                      # console; also converts to a matching X11 layout unless --no-convert
localectl set-x11-keymap gb pc105 "" ctrl:nocaps
localectl list-x11-keymap-layouts; localectl list-x11-keymap-variants de
```
Test without persisting: `loadkeys de-latin1` (console), `setxkbmap gb` (X11 session).

## 3. Debian/Ubuntu specifics
`/etc/default/keyboard` (`XKBLAYOUT="gb"`, `XKBVARIANT=`, `XKBOPTIONS=`) drives both console (via
`console-setup`) and X. Change with `dpkg-reconfigure keyboard-configuration` then
`setupcon` (console).

## 4. Boot-time (LUKS) prompt
The initramfs carries its own copy of the keymap:
- dracut-based systems (RHEL/Fedora): the keymap comes from `rd.vconsole.keymap=` on the kernel command line, or from `/etc/vconsole.conf` as written into the image; rebuild with `dracut --regenerate-all` (add `-f` to overwrite existing images).
- Debian/Ubuntu: regenerate the initramfs with the distribution tool after changing `/etc/default/keyboard`.
A mismatch here is the classic "LUKS password correct but rejected at boot".

## 5. Console font (HiDPI, special characters)
```bash
setfont ter-132n            # test; the font must be installed
# /etc/vconsole.conf: FONT=ter-132n   (Debian: FONTFACE/FONTSIZE in /etc/default/console-setup)
```

## Gotchas
- Passwords with layout-dependent characters (`@`, `"`, `#`, `\`) are the ones that fail; keep emergency passwords layout-neutral.

## Verify
- [ ] `localectl status` shows the intended VC keymap and X11 layout; typing `@"#\|` on a TTY produces the right characters.
- [ ] After regenerating the initramfs, the LUKS prompt (or `rd.break` shell) uses the same layout.

## Checked
2026-10-27. Checked against systemd localectl(1) and vconsole.conf(5) (current main), dracut.cmdline(7) and dracut(8) (dracut-ng main), and Debian keyboard(5) and console-setup(5) (trixie). Confirmed: /etc/vconsole.conf holds KEYMAP and FONT; set-keymap also sets the X11 mapping unless --no-convert, and set-x11-keymap takes LAYOUT MODEL VARIANT OPTIONS; the list-keymaps and list-x11-keymap-* verbs; rd.vconsole.keymap and rd.vconsole.font; dracut --regenerate-all; /etc/default/keyboard with XKBLAYOUT, XKBVARIANT, XKBOPTIONS read by setupcon and shared by console and X; FONTFACE and FONTSIZE in console-setup. Removed: the 00-keyboard.conf path, the Debian update-initramfs keyboard claim, the terminus package name and the Wayland and remote-console remarks, which the documentation does not cover.

Method: documentation only; no commands were run.
