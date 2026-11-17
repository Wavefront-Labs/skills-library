---
id: computing-software.software-engineering.typescript.local-package-development-link-and-pack
name: local-package-development-link-and-pack
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, npm-link, npm-pack, file-dependencies, yalc, duplicate-react, npm]
level: practitioner
status: verified
description: "Test a library inside an app before publishing: npm link and its duplicate-dependency traps, file: dependencies, npm pack tarballs, yalc, and workspaces as the long-term answer."
sources: ["https://docs.npmjs.com/cli/v10/commands/npm-link", "https://docs.npmjs.com/cli/v10/commands/npm-pack", "https://docs.npmjs.com/cli/v10/configuring-npm/package-json#local-paths", "https://github.com/wclr/yalc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local package development: link and pack

**Goal:** try unpublished library changes in a consuming app with behaviour identical
to a real install.

## npm link (fast, leaky)
```bash
cd ~/src/ui-kit && npm link            # global symlink to this package
cd ~/src/app && npm link @acme/ui-kit  # app/node_modules/@acme/ui-kit -> ~/src/ui-kit
npm unlink @acme/ui-kit && npm install # undo
```
Traps:
- The library resolves its **own** `node_modules`, so peer deps (react, graphql, styled-components)
  load twice -> "Invalid hook call", `instanceof` failures. Fix by aliasing in the bundler
  (`resolve.alias` / Vite `resolve.dedupe: ["react"]`, which forces listed dependencies to resolve to one copy from the project root per the Vite docs) or linking the app's react into the library.
- Symlinks confuse some tools: Jest does not follow symlinks when crawling unless `haste.enableSymlinks` is set (not usable with watchman, per the Jest docs); Node has `--preserve-symlinks` and TypeScript has `preserveSymlinks` to change how symlinked files resolve.
- Running `npm install <something>` in the app later silently removes the link (tested: `node_modules/@acme/ui-kit` vanished).
- Tests the source tree, not what `files`/`exports` would publish.

## file: dependency
```json
"dependencies": { "@acme/ui-kit": "file:../ui-kit" }
```
npm symlinks directories (same peer-dep issue); pointing at a tarball copies instead (tested: `npm install ../lib/acme-ui-kit-2.1.0.tgz` produced a real `dist/` and `package.json`, no symlink).

## npm pack (most faithful)
```bash
cd ui-kit && npm run build && npm pack            # acme-ui-kit-2.1.0.tgz, exactly what publish would upload
cd ../app && npm install ../ui-kit/acme-ui-kit-2.1.0.tgz
```
Catches missing files in `files`, broken `exports`, missing build output. Re-pack after each change.

## yalc (pack + copy workflow)
```bash
npx yalc publish            # in the library (runs prepublish scripts, copies to ~/.yalc)
npx yalc add @acme/ui-kit   # in the app: copies into .yalc/ and points package.json at it
npx yalc push               # library: update all consuming apps after changes
```
Real copies, no symlink issues; remember to `yalc remove --all` before committing. (Ran with yalc 1.0.0-pre.53: `add` wrote `"@acme/ui-kit": "file:.yalc/@acme/ui-kit"` into package.json and `remove --all` reverted it.)

## Long-term: workspaces
If you change library and app together often, put them in one repo with npm/pnpm workspaces;
pnpm's `workspace:` protocol and `injected` dependencies handle peer deps correctly.

## Verify
- [ ] Before publishing, the app passes its tests against an `npm pack` tarball.
- [ ] `npm ls react` in the app shows a single copy while testing the library.
