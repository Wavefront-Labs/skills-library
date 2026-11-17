---
id: computing-software.web-development.vite.server-fs-access-origin
name: server-fs-access-origin
category: computing-software
field: web-development
product: vite
tags: [server-fs-strict, server-fs-allow, server-fs-deny, server-origin, sourcemap-ignore-list]
level: advanced
status: docs-checked
description: "Restrict files served via /@fs/ with server.fs strict, allow and deny lists, searchForWorkspaceRoot, plus server.origin and server.sourcemapIgnoreList."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/server-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`server.fs.strict` (default `true`): restrict serving files outside the workspace root.

`server.fs.allow` (`string[]`): directories or files servable via `/@fs/`; others get 403 unless imported from an allowed file. Default is the detected workspace root (`workspaces` in `package.json`, `lerna.json` or `pnpm-workspace.yaml`), else the project root. Setting it disables auto detection; extend it with `searchForWorkspaceRoot`:

```js
fs: { allow: [searchForWorkspaceRoot(process.cwd()), '/path/to/custom/allow_directory'] }
```

`server.fs.deny`: picomatch blocklist, higher priority than allow. Default `['.env', '.env.*', '*.{crt,pem,key,p12,pfx,cer,der}', '.npmrc', '.yarnrc.yml', '**/.git/**']`. It does not apply to the public directory. It is matched against the module id with and without query; a plugin load hook or symlink may reach denied files by another path, so list alternatives too.

`server.origin`: origin of generated asset URLs in dev, e.g. `'http://127.0.0.1:8080'`.

`server.sourcemapIgnoreList`: `false` or `(sourcePath, sourcemapPath) => boolean` populating `x_google_ignoreList`; default ignores paths with a `node_modules` segment. It receives absolute paths and is set independently from the Rolldown output option.

## Checked

2026-11-04. Confirmed against the Vite server options page (docs/config/server-options.md): fs.strict, fs.allow workspace detection and searchForWorkspaceRoot, fs.deny default list and notes, origin, sourcemapIgnoreList. Nothing removed.

Method: documentation only; no commands were run.
