---
id: computing-software.systems-network-administration.incus.instance-console
name: instance-console
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, console, vga, spice, show-log, boot-debugging, remote-viewer]
level: intro
status: docs-checked
description: "Attach to an Incus instance console for boot debugging: incus console, --show-log, start --console, and the graphical --type vga console with a SPICE client."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_console.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance console

- `incus console <instance>` attaches to an interactive console; it is available from boot, so use it to see boot messages.
- `incus console <instance> --show-log` prints the console log.
- `incus start <instance> --console` attaches as it starts; `--console=vga` requests the graphical console.
- VMs: `incus console <vm> --type vga` gives graphical output. It needs a SPICE client: `remote-viewer` (virt-viewer package) or `spicy` (spice-client-gtk or spice-gtk-tools).
- The graphical console works even when `incus-agent` is not running or installed.

## Checked

2026-11-04: confirmed against the Incus console how-to (console, `--show-log`, `start --console`, `--console=vga`, `--type vga`, SPICE clients and packages). Nothing removed.

Method: documentation only; no commands were run.
