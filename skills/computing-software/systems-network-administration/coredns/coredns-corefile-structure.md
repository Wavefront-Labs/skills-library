---
id: computing-software.systems-network-administration.coredns.coredns-corefile-structure
name: coredns-corefile-structure
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, corefile, configuration, server-block, plugin]
level: intro
status: docs-checked
description: "Understand how a CoreDNS Corefile is organised into server blocks, plugins and directives, and how comments and the -conf flag work."
sources:
  - https://coredns.io/manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read and write a Corefile that CoreDNS parses correctly.

When started without the `-conf` flag, CoreDNS looks for a file named `Corefile` in the current directory. The file consists of one or more server blocks. Each server block lists one or more plugins, and a plugin may take directives, either inline or in its own braces plugin block.

```
. {
    plugin {
        # plugin block with directives
    }
}
```

Comments start with `#`; the rest of the line is ignored.

Key rules from the manual:
- The binaries the project provides have every plugin listed in plugin.cfg compiled in. Adding or removing plugins needs a recompile, so most users only edit the Corefile.
- The order in which plugins appear in the Corefile does NOT decide the order in which they run. Execution order is fixed by plugin.cfg at build time.
- Environment variables can be substituted anywhere, and the import plugin can appear anywhere, including above the first server block.

Failure mode: a plugin name placed outside a server block is parsed as a zone name. The manual's example is `health` at the top of the file followed by `. { whoami }`, which fails with the cryptic error `Unknown directive '.'`, because health was read as the start of a server block.

## Checked

2026-11-08. Read the configuration manual page in full; all claims match it.

Method: documentation only; no commands were run.
