---
id: computing-software.software-engineering.debugging.vscode-launch-configurations
name: vscode-launch-configurations
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, debuggers, breakpoints, launch-json, vscode-debugging, attach, compound-launch, debugpy]
level: practitioner
status: docs-checked
description: "Write VS Code launch.json configurations: launch versus attach, common attributes, variables, compounds, preLaunchTask, serverReadyAction and attach mappings."
sources: ["https://code.visualstudio.com/docs/debugtest/debugging", "https://code.visualstudio.com/docs/debugtest/debugging-configuration", "https://code.visualstudio.com/docs/python/debugging", "https://code.visualstudio.com/docs/nodejs/nodejs-debugging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VS Code launch configurations

**Goal:** repeatable debugging of an app or an already running process, with the configuration versioned in the repo.

## Anatomy
`.vscode/launch.json` (a user-level `launch` setting makes configurations available across workspaces):
```jsonc
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Server",
      "skipFiles": ["<node_internals>/**"],
      "program": "${workspaceFolder}/server.js",
      "preLaunchTask": "${defaultBuildTask}"
    },
    {
      "type": "node",
      "request": "launch",
      "name": "Client",
      "program": "${workspaceFolder}/client.js"
    }
  ],
  "compounds": [
    { "name": "Server and Client", "configurations": ["Server", "Client"], "stopAll": true }
  ]
}
```

## Key fields (debugging-configuration page)
- `type` (which debugger, e.g. `node`), `request` (`launch` starts the app and attaches; `attach` connects to an app already running in debug mode) and `name` (dropdown label) are on every configuration.
- Common to all: `presentation`, `preLaunchTask` (a label from `tasks.json` or `${defaultBuildTask}`), `postDebugTask`, `internalConsoleOptions`, `serverReadyAction`.
- Usually debugger-specific: `program`, `args`, `env` / `envFile`, `cwd`, `port`, `stopOnEntry`, `console` (`internalConsole`, `integratedTerminal`, `externalTerminal`). Use IntelliSense after setting `type` to see the supported properties.
- Variables: `${workspaceFolder}`, `${file}`, `${env:Name}`. Each element of `args` stays one argument after substitution, even with spaces; do not add escaped quotes.
- `windows`, `linux` and `osx` sections override properties per OS; `type` cannot be platform-specific.
- Compounds start several configurations in parallel; with `stopAll: true`, stopping one session stops all. A compound can have its own `preLaunchTask`.
- `serverReadyAction` matches program output with a `pattern` regex and builds a URI via `uriFormat` (default `http://localhost:%s`); `action` can be `openExternally`, `debugWithChrome`, `debugWithEdge` or `startDebugging`.
- Shell operators such as `<` or `>` in `args` are passed as literal arguments unless the debugger runs the target through a shell. For stdin, set `console` to a terminal, or start the app manually and use an attach configuration.

## Python and Node specifics
- Python attach uses `"type": "debugpy"`, `"request": "attach"` with a `connect` host and port, and `pathMappings` with `localRoot` and `remoteRoot` for remote or container code (python debugging page).
- Node: `skipFiles` is an array of glob patterns for scripts to skip stepping into; `envFile` loads variables from a file; remote attach needs correct `localRoot` and `remoteRoot` so paths map between workspace and host (nodejs-debugging page).

## Breakpoints
Logpoints write a message to the Debug Console without pausing; put expressions in braces such as `User ID: {user.id}`. They need debugger support, and can have conditions and hit counts.

## Troubleshooting
No configurations: check a folder is open, `configurations` is valid, the debugger extension for `type` is installed, and `presentation.hidden` is not true. Red squiggles: the property is not supported for that `type`/`request`. Wrong app starting: check `program`, `cwd`, `args`, env and `preLaunchTask`; for attach, the target must run in debug mode on the matching port.

## Checked
2026-11-09. Read the debugging-configuration page in full, the logpoint sections of the debugging and Node pages, and searched the Python and Node pages for debugpy, connect, pathMappings, localRoot/remoteRoot, envFile and skipFiles. Removed as unconfirmed: Go and C++ (`cppdbg`, CodeLLDB) configurations, the uvicorn and pytest examples, `justMyCode`, `substitutePath`, data breakpoints and the fresh-clone self-check.
Method: documentation only; no commands were run.
