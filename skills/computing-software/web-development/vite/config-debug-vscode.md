---
id: computing-software.web-development.vite.config-debug-vscode
name: config-debug-vscode
category: computing-software
field: web-development
product: vite
tags: [debug-config, vite-temp-sourcemaps, vscode-launch-json]
level: advanced
status: docs-checked
description: "Debug vite.config and plugin hooks in VS Code: prefer --configLoader native, or map the node_modules/.vite-temp source maps for the bundle loader."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Most reliable: start with the native loader.

```bash
vite --configLoader native
```

It runs the original config file directly, so breakpoints in the config and in plugin hooks such as `transform` map to source. It needs a runtime supporting your config syntax (Node.js 22.18+ for TypeScript).

With the `bundle` loader (the current default), Vite writes the bundled config to `node_modules/.vite-temp` with an inline source map. Allow that directory:

JavaScript Debug Terminal, in `.vscode/settings.json`:

```json
{
  "debug.javascript.terminalOptions": {
    "resolveSourceMapLocations": [
      "${workspaceFolder}/**",
      "!**/node_modules/**",
      "**/node_modules/.vite-temp/**"
    ]
  }
}
```

That setting does not affect Run and Debug launch configurations. For those, put the same `resolveSourceMapLocations` list in a `.vscode/launch.json` configuration (type `node`, `runtimeExecutable: npm`, `runtimeArgs: ["exec", "vite", "--configLoader", "bundle"]`, `sourceMaps: true`).

## Checked

Date: 2026-11-07. Read config/index.md in full, mainly Debugging the Config File in VS Code: `--configLoader native`, Node.js 22.18+ for TypeScript, bundle loader writing to `node_modules/.vite-temp`, the `resolveSourceMapLocations` list for the Debug Terminal and the launch.json fields. All matched; nothing trimmed.

Method: documentation only; no commands were run.
