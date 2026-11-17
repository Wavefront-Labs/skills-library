---
id: computing-software.software-engineering.pnpm.only-allow-pnpm
name: only-allow-pnpm
category: computing-software
field: software-engineering
product: pnpm
tags: [only-allow-pnpm, enforce-package-manager, preinstall-guard, block-npm-yarn]
level: intro
status: docs-checked
description: "Stop contributors running npm install or yarn in a pnpm project with the only-allow preinstall script, or pin the manager through devEngines.packageManager instead."
sources:
  - https://pnpm.io/only-allow-pnpm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add a `preinstall` script:

```json
{
  "scripts": {
    "preinstall": "npx only-allow pnpm"
  }
}
```

Whenever someone runs `npm install` or `yarn`, they get an error and installation does not proceed.

pnpm skips the script when it is exactly `npx only-allow pnpm`, so `pnpm install` is not slowed down. A different string runs normally.

To pin the package manager without any script, declare `devEngines.packageManager` in `package.json` (supports version ranges); see `computing-software.software-engineering.pnpm.package-json-engines-and-runtime`.

## Checked

2026-11-04. Confirmed the preinstall script, the error on npm install or yarn, the exact-string skip and the devEngines.packageManager pointer against pnpm.io/only-allow-pnpm. Removed the unsourced closing Check line and the unsourced claims that devEngines supports onFail on this page (kept in the linked skill).

Method: documentation only; no commands were run.
