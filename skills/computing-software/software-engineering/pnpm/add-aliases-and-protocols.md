---
id: computing-software.software-engineering.pnpm.add-aliases-and-protocols
name: add-aliases-and-protocols
category: computing-software
field: software-engineering
product: pnpm
tags: [npm-alias, jsr, protocol-prefix, package-url, purl, crate, pypi, add-lockfile-only]
level: practitioner
status: docs-checked
description: "Add packages under an alias or from other ecosystems: npm: aliases, jsr:, workspace: and protocol-prefixed selectors, pkg: Package URLs, crate: and pypi: prefixes."
sources:
  - https://pnpm.io/cli/add
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Alias an npm package under another local name:

```sh
pnpm add <alias>@npm:<package>@<version-or-tag>
pnpm add babel-core@npm:@babel/core@8.0.6
```

`babel-core` becomes the dependency name while `@babel/core@8.0.6` is resolved. `npm:` is the alias protocol, not a named registry; registry routing follows the target package's config.

Protocol in front of the name:

```sh
pnpm add jsr:@scope/pkg
pnpm add npm:pkg@^1.0.0
pnpm add workspace:pkg@*
```

Other ecosystems:
- `pnpm add crate:serde` (Cargo) and `pnpm add pypi:httpx` (Python).
- Package URLs (v12.5.0): `pnpm add pkg:npm/express@4.18.2`, `pkg:cargo/...`, `pkg:pypi/...`, saved to `package.json`, `Cargo.toml` and `pyproject.toml`. `pkg` is reserved and cannot be a named registry alias.
- `--save-build` installs `crate:` packages as Cargo build dependencies.

Also: `--lockfile-only` updates `package.json` and the lockfile without writing `node_modules`; `--registry=<url>` overrides the registry for one add.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/add: npm: alias syntax and babel-core example, protocol-prefixed selectors, crate:/pypi: prefixes, Package URLs (v12.5.0), pkg reserved, --save-build, --lockfile-only, --registry. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
