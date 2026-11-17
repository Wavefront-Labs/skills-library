---
id: computing-software.software-engineering.wails.ide-vscode-debug-config
name: ide-vscode-debug-config
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, vscode, debugging, ide, launch-json, tasks-json]
level: practitioner
status: docs-checked
description: "Generate and adapt the VS Code tasks.json and launch.json for debugging a Wails project, including frontend install and build steps."
sources: [https://wails.io/docs/guides/ides]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: debug a Wails app from VS Code (Goland is also supported but the page gives no detail).

## Generate
Create the project with the `-ide vscode` flag. Files go to `.vscode/`: `tasks.json` and `launch.json`.

## Generated files (default vanilla project)
`tasks.json` builds a dev binary with debug-friendly flags:

```json
{
  "label": "build",
  "type": "shell",
  "options": { "cwd": "${workspaceFolder}" },
  "command": "go",
  "args": ["build", "-tags", "dev", "-gcflags", "all=-N -l", "-o", "build/bin/myproject.exe"]
}
```

`launch.json` runs that binary after the `build` task:

```json
{
  "name": "Wails: Debug myproject",
  "type": "go",
  "request": "launch",
  "mode": "exec",
  "program": "${workspaceFolder}/build/bin/myproject.exe",
  "preLaunchTask": "build",
  "cwd": "${workspaceFolder}",
  "env": {}
}
```

## Frontend build step
The default tasks file has no `npm install` / `npm run build` step. For templates with a frontend (the page uses svelte), add two npm tasks with `"options": {"cwd": "${workspaceFolder}/frontend"}` (labels `npm install` with script `install`, and `npm run build` with script `build`, each with presentation `clear: true`, `panel: shared`, `showReuseMessage: false`, `problemMatcher: []`) and make the `build` task depend on them:

```json
"dependsOn": ["npm install", "npm run build"]
```

The `-o` target in the example is `build/bin/vscode.exe` for that project; keep it identical to the `program` path in `launch.json`.

## Gaps
The page notes automatic generation of the install/build steps is a hoped-for future enhancement. Non-Windows binary names are not specified.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "IDEs" guide.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
