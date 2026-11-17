---
id: computing-software.software-engineering.typescript.semver-ranges-and-peer-dependencies
name: semver-ranges-and-peer-dependencies
category: computing-software
field: software-engineering
product: typescript
tags: [npm, semver-ranges, peer-dependencies, caret-range, tilde-range, dependency-types, optional-dependencies, eresolve, legacy-peer-deps]
level: practitioner
status: verified
description: "Choose npm version ranges and dependency types correctly: ^ vs ~ vs exact, 0.x semantics, peerDependencies for plugins, and fixing ERESOLVE conflicts."
sources: ["https://docs.npmjs.com/cli/configuring-npm/package-json#dependencies", "https://docs.npmjs.com/cli/configuring-npm/package-json#peerdependencies", "https://github.com/npm/node-semver#ranges", "https://semver.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SemVer ranges and peer dependencies

**Goal:** dependency declarations that let consumers dedupe and update safely, without
installing two copies of React or breaking on a minor bump.

## Range syntax
| Range | Allows | Note |
|---|---|---|
| `^1.4.2` | `>=1.4.2 <2.0.0` | npm default |
| `^0.4.2` | `>=0.4.2 <0.5.0` | for 0.x, caret locks the MINOR |
| `^0.0.3` | exactly `0.0.3` | |
| `~1.4.2` | `>=1.4.2 <1.5.0` | patch only |
| `1.4.2` | exact | |
| `>=1.4 <3` | explicit | useful for peer deps spanning majors |
| `1.x`, `*` | wide | avoid `*` |
Check: `npx semver -r "^0.4.2" 0.5.0` (prints nothing and exits 1 if out of range; `0.4.9` prints `0.4.9`). Ranges in this table were confirmed with `semver.Range` (7.x): e.g. `^1.4.2` is `>=1.4.2 <2.0.0-0`.
Pre-releases (`2.0.0-beta.1`) only match ranges that mention a pre-release of the same version.

## Which dependency field
| Field | Use for |
|---|---|
| `dependencies` | needed at runtime by your code |
| `devDependencies` | build/test tooling, types for your own build |
| `peerDependencies` | the host framework your plugin/library plugs into (react, eslint, typescript) |
| `optionalDependencies` | platform-specific binaries; install failure tolerated |
| `peerDependenciesMeta: { x: { optional: true } }` | integrations you support but don't require |

## Peer dependencies
A React component library must NOT list `react` in `dependencies` (two Reacts ->
"Invalid hook call"). Declare a wide peer range plus a devDependency for local testing:
```json
"peerDependencies": { "react": "^18.2 || ^19" },
"devDependencies": { "react": "^19.0.0" }
```
npm 7+ installs peers automatically and errors (`ERESOLVE`) on conflicts (tested: react ^18.2 with react-dom ^19 fails; `--legacy-peer-deps` then installs react 18.3.1 and `npm ls` flags it `invalid`).

## Fixing ERESOLVE
1. Read the message: which package wants which peer range.
2. Upgrade the plugin to a version supporting your framework version, or align versions.
3. Temporary escape: `overrides` in package.json for the specific package; last resort
   `--legacy-peer-deps` (silently ignores peers; can produce runtime breakage).

## Apps vs libraries
- Libraries: wide ranges (caret) so consumers dedupe.
- Apps: caret ranges plus a committed lockfile is the norm; the lockfile provides pinning.

## Verify
- [ ] `npm ls react` shows a single copy.
- [ ] `npm install` runs without ERESOLVE or `--legacy-peer-deps`.
