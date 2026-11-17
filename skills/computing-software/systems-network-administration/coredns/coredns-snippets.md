---
id: computing-software.systems-network-administration.coredns.coredns-snippets
name: coredns-snippets
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, snippets, import, corefile, reuse]
level: practitioner
status: docs-checked
description: "Define a reusable snippet with a parenthesised name and include it in several server blocks using import."
sources:
  - https://coredns.io/manual/configuration/
  - https://coredns.io/plugins/import/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid repeating the same plugin lines in every server block.

A snippet is a block labelled with a single token in parentheses, then included with the import plugin:

```
(snip) {
    prometheus
    log
    errors
}

. {
    whoami
    import snip
}
```

Details:
- The label is the name in parentheses, and `import snip` refers to it without the parentheses.
- The imported contents replace the import line, as if that text appeared there to begin with.
- The manual's example defines the snippet at the top level of the Corefile, beside the server blocks.
- A Corefile may contain at most 10000 import statements; a glob pattern counts as one. The limit protects against recursive imports.
- The import plugin can also include files (path relative to the Corefile, globs allowed). A missing specific file is an error; an empty glob is not.

Example of importing a shared file inside a block:

```
. {
    import config/common.conf
}
```

Environment variables can be used anywhere in the Corefile, so they can be combined with imports to vary a configuration per deployment.

## Checked

2026-11-08. Read the configuration manual page and the import plugin README in full. Removed an unsupported claim about once-only plugins and added the import behaviour and 10000 import limit from the import README.

Method: documentation only; no commands were run.
