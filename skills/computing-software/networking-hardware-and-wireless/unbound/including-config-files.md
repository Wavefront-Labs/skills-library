---
id: computing-software.networking-hardware-and-wireless.unbound.including-config-files
name: including-config-files
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, include, include-toplevel, glob, config-layout]
level: practitioner
status: docs-checked
description: "Split an Unbound configuration across files with include and include-toplevel, including chroot path rules and wildcards."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# including config files
`include:` may appear anywhere and takes one file name. Processing continues as if the text of that file were copied in at that point, so the included file continues whatever section clause was active.

`include-toplevel:` instead closes any active section clause. The included file must then start with its own section clauses, and a section clause must follow the directive immediately.

Paths: with `chroot` in use, give full paths. Relative paths work only if the start directory equals the chroot/working directory, or if `directory:` is set before the `include` line.

Wildcards can pull in several files at once; the syntax is that of glob(7).

Section clauses may be repeated, including inside included files, which suits one file per forward-zone, view or rpz policy.

## Checked

2026-11-08. Read the Including Files section of the unbound.conf manual page and the directory entry; all claims match them. The rest of the page was not read.

Method: documentation only; no commands were run.
