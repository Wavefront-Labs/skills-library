---
id: computing-software.systems-network-administration.linux.grub-and-kernel-serial-console
name: grub-and-kernel-serial-console
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, grub, serial-console, grub-serial, console-ttys0, getty, ipmi-sol, kernel-cmdline, headless]
level: practitioner
status: docs-checked
description: "Get GRUB menus, kernel messages and a login prompt on a serial port (ttyS0/IPMI SOL/cloud serial console): GRUB_TERMINAL, console= ordering and serial-getty."
sources:
  - https://www.kernel.org/doc/html/latest/admin-guide/serial-console.html
  - https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-getty-generator.html
  - https://github.com/coreos/grub/blob/master/docs/grub.texi
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serial console for GRUB and the kernel

**Goal:** a headless server (IPMI SOL, iLO/iDRAC VSP, cloud serial console, KVM `virsh console`)
shows the boot menu, kernel log, emergency shell and a login on the serial line.

## /etc/default/grub
```
GRUB_TERMINAL="console serial"
GRUB_SERIAL_COMMAND="serial --unit=0 --speed=115200 --word=8 --parity=no --stop=1"
GRUB_CMDLINE_LINUX="... console=tty0 console=ttyS0,115200n8"
GRUB_TIMEOUT=5
GRUB_TIMEOUT_STYLE=menu
```
Regenerate the configuration with `grub-mkconfig -o <path to grub.cfg>` (distribution wrappers: `update-grub`, `grub2-mkconfig`).

## Kernel console= rules
- Multiple `console=` allowed; output appears on all of them, and when each device type is named once
  **/dev/console is the LAST one** (kernel serial-console doc) — put `ttyS0` last for headless use.
  If the same device type is repeated, the first registered device wins and graphical consoles register before serial ones.
- Format `console=ttyS0,BBBBPNF` (speed, parity n/o/e, bits, flow control `r`); default 9600n8, maximum baud rate 115200.
- ttyS0 is the first serial port (GRUB unit 0 is COM1), ttyS1 the second. Check which port your BIOS or BMC console redirection uses.
- The speed must match the BIOS redirection and the client terminal.

## Login prompt
systemd-getty-generator starts `serial-getty@.service` automatically on kernel consoles that are not provided by the virtual console subsystem.
For another port: `systemctl enable --now serial-getty@ttyS1.service`.

## Gotchas
- `GRUB_TERMINAL=serial` only (no `console`) hides the menu on the local VGA screen.
- `quiet` still suppresses most kernel output on serial — drop it while debugging.
- No output at all usually means the wrong port or unit.

## Verify
- [ ] `cat /proc/cmdline` shows `console=ttyS0,115200n8` last.
- [ ] `systemctl status serial-getty@ttyS0` active (when ttyS0 is a console); a reboot shows the GRUB menu on the serial client.

## Checked
2026-10-27. Checked against the Linux kernel serial-console admin guide and kernel-parameters (quiet: disable most log messages), the GRUB manual source (coreos/grub docs/grub.texi, a mirror of upstream: GRUB_TERMINAL overriding input and output, GRUB_SERIAL_COMMAND defaulting to serial, the serial command options with unit 0 as COM1, GRUB_TIMEOUT_STYLE menu) and systemd-getty-generator(8). Confirmed: console= format and maximum 115200; the last console used for /dev/console with the repeated-type exception; GRUB_TERMINAL and GRUB_SERIAL_COMMAND semantics; serial-getty generation for kernel consoles. Removed: the 0x3f8 address, IPMI port guesses, client tool examples, ARM and Xen device names, the grubby command, the --rtscts remark and distribution-specific grub.cfg paths, which the documents do not cover.

Method: documentation only; no commands were run.
