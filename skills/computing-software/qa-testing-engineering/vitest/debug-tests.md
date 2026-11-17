---
id: computing-software.qa-testing-engineering.vitest.debug-tests
name: debug-tests
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [debug-tests, inspect-brk, vscode-launch-config, chrome-inspect]
level: practitioner
status: docs-checked
description: "Debug Vitest tests in VS Code, IntelliJ or Chrome DevTools: JavaScript Debug Terminal, launch config, --inspect-brk, no file parallelism and timeout zero."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/debugging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before stopping at breakpoints, avoid timeouts and parallel files:
- `--test-timeout=0`
- `--no-file-parallelism`

VS Code: the official extension has a "Debug Tests" button. Quick alternative: open a `JavaScript Debug Terminal` and run `npm run test` or `vitest`. Or add a launch config:

```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug Current Test File",
  "autoAttachChildProcesses": true,
  "skipFiles": ["<node_internals>/**", "**/node_modules/**"],
  "program": "${workspaceRoot}/node_modules/vitest/vitest.mjs",
  "args": ["run", "${relativeFile}"],
  "smartStep": true,
  "console": "integratedTerminal"
}
```

Node inspector (Chrome DevTools via `chrome://inspect`):

```sh
vitest --inspect-brk --no-file-parallelism
vitest --inspect-brk --browser --no-file-parallelism
```

In browser mode the default debug port is 9229; override with `--inspect-brk=127.0.0.1:3000`. In watch mode, `--isolate false` keeps the debugger open across reruns.

IntelliJ IDEA: create a vitest run configuration with the working directory set to the project root, then run it in debug mode.

## Checked

2026-11-04. Confirmed against guide/debugging.md: the tip options, Debug Terminal, launch config, inspector commands, default port 9229 and the `--inspect-brk` override, `--isolate false` in watch mode, IntelliJ settings.

Method: documentation only; no commands were run.
