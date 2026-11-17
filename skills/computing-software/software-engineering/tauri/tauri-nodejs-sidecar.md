---
id: computing-software.software-engineering.tauri.tauri-nodejs-sidecar
name: tauri-nodejs-sidecar
category: computing-software
field: software-engineering
product: tauri
tags: [nodejs-sidecar, tauri, sidecar, shell-plugin]
level: practitioner
status: docs-checked
description: "Package a Node.js app into a self-contained binary with pkg and run it as a Tauri sidecar through the shell plugin on desktop."
sources:
  - "https://v2.tauri.app/learn/sidecar-nodejs/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js as a Tauri sidecar

Goal: ship a Node.js program as a binary sidecar so end users need no Node.js. Desktop only. Needs a Tauri app with the shell plugin set up and initialized.

## Method

1. In a new `sidecar-app` directory in the Tauri app root, run `npm init` (or yarn/pnpm) and add `@yao-pkg/pkg` as a dev dependency. Any tool that compiles JS or TS to a binary works.
2. `sidecar-app/index.js` reads `process.argv` and writes to stdout (short-lived, one command at a time; use other IPC for long-lived processes):

```js
const command = process.argv[2];
switch (command) {
  case 'hello':
    const message = process.argv[3];
    console.log(`Hello ${message}!`);
    break;
  default:
    console.error(`unknown command ${command}`);
    process.exit(1);
}
```

3. Add `"build": "pkg index.ts --output my-sidecar"` (as the page writes it, although the file created in step 2 is `index.js`) to `scripts` in `package.json` and run it. Then rename the binary to the sidecar pattern `my-sidecar-<target-triple>` (plus `.exe` on Windows) inside `src-tauri/binaries`. The page's `rename.js` gets the triple from `rustc --print host-tuple` (Rust 1.84.0+; older versions parse `rustc -vV` for `host: (\S+)`) and uses `fs.renameSync` to `../src-tauri/binaries/my-sidecar-${targetTriple}${ext}`. Run `node rename.js` from `sidecar-app`; create the `binaries` dir first.
4. Allow it in `src-tauri/capabilities/default.json`:

```json
{
  "identifier": "shell:allow-execute",
  "allow": [{ "args": true, "name": "binaries/my-sidecar", "sidecar": true }]
}
```

`args` may instead be an array such as `["hello"]`.
5. Register it in `src-tauri/tauri.conf.json`:

```json
{ "bundle": { "externalBin": ["binaries/my-sidecar"] } }
```

6. Run it from JavaScript:

```js
import { Command } from '@tauri-apps/plugin-shell';
const command = Command.sidecar('binaries/my-sidecar', ['hello', 'Tauri']);
const output = await command.execute();
console.log(output.stdout)
```

Or from Rust with `app.shell().sidecar("my-sidecar").unwrap().arg(cmd).arg(message)` and `.output().await`, exposed as a Tauri command.
7. Run `tauri dev` and open DevTools (F12, or Cmd+Option+I on macOS) to see the output.

## Checked

Checked 2026-11-08 against the Tauri v2 Node.js sidecar page: @yao-pkg/pkg, index.js, build script, rename.js and the host-tuple note, shell:allow-execute capability, externalBin entry, JavaScript and Rust invocation, and DevTools shortcuts. Noted the index.ts versus index.js inconsistency on the page. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
