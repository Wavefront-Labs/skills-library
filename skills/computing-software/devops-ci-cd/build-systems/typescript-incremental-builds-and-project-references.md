---
id: computing-software.devops-ci-cd.build-systems.typescript-incremental-builds-and-project-references
name: typescript-incremental-builds-and-project-references
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, tsbuildinfo, project-references, incremental-builds]
level: practitioner
status: docs-checked
description: "Speed up TypeScript builds with incremental compilation (.tsbuildinfo), project references and tsc --build in monorepos, and cache build info correctly in CI."
sources: ["https://www.typescriptlang.org/docs/handbook/project-references.html", "https://www.typescriptlang.org/tsconfig/#incremental", "https://www.typescriptlang.org/tsconfig/#composite", "https://www.typescriptlang.org/tsconfig/#tsBuildInfoFile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TypeScript incremental builds and project references

## incremental
```json
{ "compilerOptions": { "incremental": true, "tsBuildInfoFile": ".cache/tsbuildinfo.json" } }
```
`incremental` saves information about the project graph from the last compilation to `.tsbuildinfo` files so the next run can skip unchanged work; `tsBuildInfoFile` sets where the file is stored.

## Project references (monorepo)
```json
// packages/api/tsconfig.json
{
  "compilerOptions": { "composite": true, "outDir": "dist", "rootDir": "src", "declaration": true },
  "references": [{ "path": "../shared" }]
}
// tsconfig.json at root (solution file)
{ "files": [], "references": [{ "path": "packages/shared" }, { "path": "packages/api" }] }
```
```bash
tsc --build            # builds referenced projects in dependency order, skipping up-to-date ones
tsc -b --verbose       # logs why each project is or is not rebuilt
tsc -b --clean         # deletes the outputs of the projects
```
`composite` makes `rootDir` default to the directory of the tsconfig, requires that every implementation file matches `include` or `files`, and requires `declaration` to be on. `tsc` does not build references unless invoked with `--build`.

## CI caching
Cache the `.tsbuildinfo` files together with the build outputs (`dist/`) so they stay consistent. Key on lockfile and tsconfig hashes; `restore-keys` allow partial reuse.

## Typecheck-only
Bundlers (Vite, esbuild, swc) do not typecheck; run `tsc -b` or `tsc --noEmit` separately in CI.

## Gotchas
- `skipLibCheck: true` skips type checking of declaration files, which saves time on large dependency trees at some cost in accuracy.

## Verify
- [ ] A second `tsc -b` with no changes finishes quickly; touching one package rebuilds it and its dependants only.

## Checked
Date: 2026-10-25. Documentation: TypeScript-Website sources (microsoft/TypeScript-Website: handbook "Project References", tsconfig reference pages for `incremental`, `composite`, `tsBuildInfoFile`, `noEmit`, `skipLibCheck`).
Confirmed: `incremental` and `.tsbuildinfo`; `tsBuildInfoFile`; `composite` constraints (`rootDir` default, `include`/`files` coverage, `declaration`); `tsc --build`, `--verbose`, `--clean`; `tsc` does not build references without `--build`; `skipLibCheck`.
Removed: the "TS 4.0+ writes build info with noEmit" claim, the explanation that build info without outputs misleads tsc, and the "path aliases give no boundaries" and "changing compilerOptions invalidates everything" gotchas (none appear in the pages read).
Method: documentation only; no commands were run.
