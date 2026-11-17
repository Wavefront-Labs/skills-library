---
id: computing-software.software-engineering.pnpm.run-scripts
name: run-scripts
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-run, run-script, script-shorthand, regex-script-selector, if-present, script-arguments, node-modules-bin]
level: intro
status: docs-checked
description: "Run package.json scripts with pnpm run: the pnpm <script> shorthand, argument passing, regex selectors, --sequential, --no-bail, --if-present and node_modules/.bin on PATH."
sources:
  - https://pnpm.io/cli/run
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pnpm run` lists scripts; `pnpm run watch` runs one. `pnpm watch` works only if the name is not a pnpm command.

Options go before the script name; anything after it is passed to the script: `pnpm run watch --no-color` runs `webpack --watch --no-color`.

Regex selector (quoted, slash-delimited, JS syntax):

```sh
pnpm run "/^watch:/"
pnpm run "/^hello:(?!b$).*$/"
```

- Matching is unanchored (`/build:.*/` matches `prebuild:web`); anchor with `^` and `$`.
- An exact script name beats regex matching; flags like `/i` fail with `ERR_PNPM_UNSUPPORTED_SCRIPT_COMMAND_FORMAT`.
- Matches run concurrently since v12.2.0 (limited by `--workspace-concurrency`), prefixed with the script name, in lexicographic order. `--sequential` / `-s` runs one at a time. With `--no-bail` all finish, then exit `ERR_PNPM_RUN_FAILED`.
- For `pnpm run`, `-s` means `--sequential`; elsewhere it stays `--reporter=silent`. `--silent` is unchanged.

`node_modules/.bin` (and the workspace root's) is on `PATH`, so installed tools run without global installs. `--if-present` avoids a failure when the script is undefined.

## Checked

2026-11-04. Confirmed the shorthand rule, argument passing, regex selector rules, v12.2.0 concurrency, --sequential, --no-bail, --if-present and the node_modules/.bin PATH note against pnpm.io/cli/run. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
