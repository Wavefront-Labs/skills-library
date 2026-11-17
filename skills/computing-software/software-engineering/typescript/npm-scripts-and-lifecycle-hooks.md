---
id: computing-software.software-engineering.typescript.npm-scripts-and-lifecycle-hooks
name: npm-scripts-and-lifecycle-hooks
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, npm-scripts, npx, lifecycle-scripts, prepare-script, cross-platform-scripts, npm]
level: practitioner
status: verified
description: "Write npm scripts that work everywhere: pre/post and lifecycle hooks (prepare, prepublishOnly), passing args, npx/npm exec, cross-platform pitfalls and install-script security."
sources: ["https://docs.npmjs.com/cli/v10/using-npm/scripts", "https://docs.npmjs.com/cli/v10/commands/npm-exec", "https://docs.npmjs.com/cli/v10/commands/npm-run-script"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# npm scripts and lifecycle hooks

**Goal:** a `scripts` block that is the project's task runner on every OS and CI,
without surprise hooks.

## Basics
```json
"scripts": {
  "build": "tsc -p tsconfig.build.json",
  "test": "vitest run",
  "lint": "eslint . && tsc --noEmit",
  "dev": "node --watch --env-file=.env src/server.ts",
  "check": "npm run lint && npm test"
}
```
- `node_modules/.bin` is on PATH inside scripts, so local tools run without `npx`.
- Pass extra args after `--`: `npm test -- --reporter=verbose`.
- `npm run` lists scripts; `npm run <s> --workspaces --if-present` runs across a monorepo.
- `npm_package_version`, `npm_lifecycle_event` and `npm_config_*` are set as environment variables for scripts. A `$npm_package_version` written in the script string is expanded only by a POSIX shell: under the Windows default `cmd.exe` it prints literally (tested), so read `process.env.npm_package_version` in Node or set `script-shell`.
- The `dev` script above runs a `.ts` file with Node's type stripping: it works on Node 24 and fails on Node 20 (both tested).

## pre/post and lifecycle scripts
- `prebuild`/`postbuild` run around `build` automatically (`--ignore-scripts` disables them).
  Explicit chaining (`"build": "npm run clean && tsc"`) is clearer.
- `prepare`: runs on local `npm install` and `npm ci`, before `npm pack/publish` (`npm publish` ran prepublishOnly, prepack, then prepare on npm 10.8), and when installed
  from git (npm docs: devDependencies are installed and `prepare` runs first). Used for husky setup or building git-installed packages.
- `prepublishOnly`: runs only before `npm publish` - put `npm run build && npm test` here.
- `preinstall`/`install`/`postinstall`: run when **your package is installed by others**. Avoid
  them in libraries; they slow installs and are a supply-chain attack vector.

## npx / npm exec
```bash
npx tsc --version                 # local bin if installed, otherwise prompts to download
npx --yes create-vite@6 my-app    # pin versions for one-off generators
npm exec --package=@biomejs/biome@2 -- biome check .
```
In CI, `npx` of an unpinned package downloads whatever is latest - pin or install it.

## Cross-platform pitfalls
Scripts run in `sh` on POSIX and `cmd.exe` on Windows by default:
- `rm -rf`, `cp`, `&` backgrounding, `$VAR` and single quotes differ. Use `rimraf`/`shx` or
  Node one-liners (`node -e "fs.rmSync('dist',{recursive:true,force:true})"`).
- Setting env vars inline (`NODE_ENV=production node x`) fails in cmd: use `cross-env` or
  `--env-file`.
- Parallel: `npm-run-all2` (`run-p lint test`) or `concurrently`.
- Or set `script-shell` in `.npmrc` to bash on Windows dev machines.

## Security
`npm ci --ignore-scripts` in CI for untrusted dependency trees (then run the scripts you need).
pnpm 10+ does not run dependency build scripts unless allowed. In pnpm 12.14 the allowlist is
`allowBuilds` in `pnpm-workspace.yaml` (`allowBuilds: { esbuild: true }`); `onlyBuiltDependencies`
no longer worked there (tested), and an install with unreviewed builds fails with
`ERR_PNPM_IGNORED_BUILDS` until you run `pnpm approve-builds`.

## Verify
- [ ] `npm run check` passes on Linux and Windows CI runners.
- [ ] Library has no install-time scripts; `prepublishOnly` builds and tests.
