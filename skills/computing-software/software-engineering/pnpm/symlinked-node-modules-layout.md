---
id: computing-software.software-engineering.pnpm.symlinked-node-modules-layout
name: symlinked-node-modules-layout
category: computing-software
field: software-engineering
product: pnpm
tags: [symlinked-node-modules, node-modules-pnpm-dir, strict-dependencies, non-flat-node-modules, virtual-store]
level: practitioner
status: docs-checked
description: "Read pnpm's node_modules layout: real files under node_modules/.pnpm, symlinks for dependencies, why only declared packages are importable, and what hoist=false does."
sources:
  - https://pnpm.io/symlinked-node-modules-structure
  - https://pnpm.io/motivation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Layout (no peer dependencies case):

```text
node_modules
├── foo -> ./.pnpm/foo@1.0.0/node_modules/foo
└── .pnpm
    ├── bar@1.0.0/node_modules/bar
    └── foo@1.0.0/node_modules
        ├── foo
        └── bar -> ../../bar@1.0.0/node_modules/bar
```

- The only real files live in `node_modules/.pnpm/<name>@<version>/node_modules/<name>`, hard-linked from the store.
- A package sits in its own `node_modules` subfolder so it can import itself and so symlinks never loop.
- Its dependencies are symlinked next to it. Node resolves a symlink to its real path, so `bar` finds its own deps beside it.
- The project root `node_modules` gets symlinks for direct dependencies only, so code cannot import undeclared packages (no phantom dependencies).
- Directory depth stays constant however deep the graph is.

Many published packages use undeclared deps, so pnpm hoists everything by default into `node_modules/.pnpm/node_modules`. Set `hoist` to `false` to disable.

For peer-dependency variants see `computing-software.software-engineering.pnpm.how-peers-are-resolved`.

## Checked

2026-11-04. Confirmed the layout, the reasons for the nested node_modules folder, the strictness benefit and the default hoisting with the hoist setting against pnpm.io/symlinked-node-modules-structure and pnpm.io/motivation.

Method: documentation only; no commands were run.
