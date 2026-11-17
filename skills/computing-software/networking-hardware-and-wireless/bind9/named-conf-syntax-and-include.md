---
id: computing-software.networking-hardware-and-wireless.bind9.named-conf-syntax-and-include
name: named-conf-syntax-and-include
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, named-conf, include, comments]
level: practitioner
status: docs-checked
description: "named.conf structure in BIND 9: one file, three comment styles, include with globs, and the main statement blocks."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# named conf syntax and include
BIND 9 is configured by a single `named.conf` file. Comments can be written in the C, C++ or shell/Perl style.

`include` inserts the specified file, or files if a valid glob expression is given, where the directive appears.

Main blocks: `options`, `acl`, `controls`, `key`, `key-store`, `logging`, `server`, `statistics-channels`, `tls`, `http`, `trust-anchors`, `dnssec-policy`, `view`, `zone`, `template`, `remote-servers`.

`rndc.conf` is a separate file; it is not required when `rndc` runs on the same system as named, and will be present when it runs from a remote host.

## Checked

2026-11-04. Read the Configuration File (named.conf) and Blocks sections of the Administrator Reference Manual: comment styles, include with glob expressions, the block list and rndc.conf note. Reworded the comment and rndc.conf sentences to match the page and removed two unconfirmed statements (fragment use, check-before-reload).

Method: documentation only; no commands were run.
