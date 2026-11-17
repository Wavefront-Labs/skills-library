---
id: computing-software.systems-network-administration.coredns.coredns-import-plugin
name: coredns-import-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, import, corefile, glob, includes]
level: practitioner
status: docs-checked
description: "Include other files or reuse named snippets in a Corefile with the import plugin, including glob patterns and the 10000 import limit."
sources:
  - https://coredns.io/plugins/import/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: split a Corefile into reusable files without duplication.

Syntax: `import PATTERN`. PATTERN is a file, a glob pattern containing `*`, or a snippet name. The contents replace the import line as if they had been written there.

Properties from the docs:
- import is unusual because it may appear outside a server block, at the top of the Corefile where an address would normally be.
- File locations are relative to the Corefile's location.
- A specific file that cannot be found is an error, but a glob pattern that matches nothing is not.
- A Corefile may contain at most 10000 import statements. A glob counts as a single import. The limit protects against recursive imports.

Example: a shared file included from a server block.

```
. {
    import config/common.conf
}
```

where `config/common.conf` holds plugin lines such as `prometheus`, `errors` and `log`.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/import/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: the failure-mode claim that the limit reports an error (the page says only that the limit protects against recursive imports).

Method: documentation only; no commands were run.
