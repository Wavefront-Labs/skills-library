---
id: computing-software.software-engineering.pnpm.runtime-set-node
name: runtime-set-node
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-runtime, runtime-set, node-version-management, deno-runtime, bun-runtime, dev-engines-runtime-save, pnpm-env-deprecated]
level: practitioner
status: docs-checked
description: "Manage Node.js, Deno and Bun with pnpm runtime set (alias rt), globally or per project, and migrate from the deprecated pnpm env use / remove / list commands."
sources:
  - https://pnpm.io/cli/runtime
  - https://pnpm.io/cli/env
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
pnpm runtime set <name> <version> [-g]
pnpm runtime set node 22 -g
pnpm runtime set node lts -g
pnpm runtime set node latest -g
pnpm runtime set node rc/22 -g       # prerelease: nightly, rc, rc/22, 22.0.0-rc.4
pnpm runtime set node argon -g       # LTS codename
pnpm runtime set deno 2 -g
pnpm runtime set bun latest -g
```

- Runtimes: `node`, `deno`, `bun`.
- Without `-g` the runtime is added to the project as `<name>@runtime:<version>`: into `devEngines.runtime` by default (`--save-dev`, `-D`) or `engines.runtime` with `--save-prod`, `-P`. pnpm then suggests `pnpm shim add <name>` so the bare command uses the project's runtime.
- Installing Node.js this way does not install the bundled `npm`, `npx` or `corepack`; use `pnpm add -g npm`.
- Release metadata is cached after signature verification, so a pinned runtime resolves without network.

Deprecated `pnpm env` mapping: `pnpm env use --global lts` becomes `pnpm runtime set node lts -g`; `pnpm env remove --global <version>` becomes `pnpm remove -g node`. `pnpm env list [range]` printed available Node versions. `env use` and `remove` required `--global`, else `ERR_PNPM_NOT_IMPLEMENTED_YET`.

## Checked

2026-11-04. Confirmed the pnpm runtime set usage and examples, save-dev and save-prod placement, the npm/npx/corepack note, metadata caching and the deprecated pnpm env mapping against pnpm.io/cli/runtime and pnpm.io/cli/env. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
