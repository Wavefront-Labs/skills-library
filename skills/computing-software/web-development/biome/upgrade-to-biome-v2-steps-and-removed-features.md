---
id: computing-software.web-development.biome.upgrade-to-biome-v2-steps-and-removed-features
name: upgrade-to-biome-v2-steps-and-removed-features
category: computing-software
field: web-development
product: biome
tags: [biome, upgrade-v2, biome-migrate, rome-removed, config-path-removed, assert-syntax, breaking-changes, biome-ignore]
level: practitioner
status: docs-checked
description: "Upgrade from Biome v1 to v2 via biome migrate --write and handle removed Rome features, --config-path and the assert import syntax."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/installation/upgrade-to-biome-v2.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Steps.** Install the v2 version pinned (`npm install --save-dev --save-exact @biomejs/biome@2.0.6`, or the pnpm/yarn/bun/deno/standalone equivalents), run `biome migrate --write`, then read the command output: it mitigates breaking changes automatically but points out any manual steps.

**Rome leftovers are gone:** rename `rome.json` to `biome.json`, `// rome-ignore` to `// biome-ignore`, `ROME_BINARY` to `BIOME_BINARY`, and change the old suppression format `// biome-ignore lint(<GROUP>/<RULE>): <explanation>` to `// biome-ignore lint/<GROUP>/<RULE>: <explanation>`.

**`--config-path` removed** from `biome lsp-proxy` and `biome start`. It overrode the configuration path for every workspace in the daemon, causing mismatches when an editor opened several projects. Use the editor setting instead: VS Code `configurationPath`, Zed `configuration_path`, for example `"./frontend/biome.json"`. Plugin authors should use the `workspace/configuration` response; Biome's LSP resolves a configuration in the workspace automatically, so leave it empty unless you use a custom path.

**`assert` import attributes no longer parse.** Replace `import x from "foo.json" assert { type: "json" }` with `with { type: "json" }` (also for `export * from "mod"`). All Node.js LTS versions, browsers and serverless runtimes support `with`.

**Editor traps.** Zed extension v0.2.0 is incompatible with Biome v1 (because of the missing `--config-path`). VS Code extension v3 connects to the Biome daemon differently; after upgrading it, using `"source.fixAll.biome": "explicit"` can produce incorrect code on save unless you upgrade the extension, close the editor, kill dangling `biome` processes, and restart the editor.

## Checked

2026-11-08. Read the upgrade-to-biome-v2 page in full. Unchanged: pinned install and migrate --write, Rome leftovers, --config-path removal and editor settings, assert to with, Zed and VS Code notes. Removed: the invented Verify step.

Method: documentation only; no commands were run.
