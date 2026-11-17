---
id: computing-software.devops-ci-cd.build-systems.monorepo-build-strategies
name: monorepo-build-strategies
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, monorepo, polyrepo, affected-targets, change-detection, nx, nx-affected, turborepo, turbo-filter, bazel, buck2, pants, lerna, pnpm-workspaces, yarn-workspaces, gradle-composite-builds, dynamic-matrix, merge-base, fetch-depth, global-inputs, namedinputs, module-boundaries, codeowners, sparse-checkout, partial-clone, scalar, internal-packages, independent-versioning]
level: advanced
status: draft
description: "Keep a monorepo's CI proportional to the change: correct affected detection, global-input traps, dynamic CI fan-out, internal package wiring, boundaries, and scaling Git checkouts."
sources: ["https://nx.dev/ci/features/affected", "https://turbo.build/repo/docs/crafting-your-repository/running-tasks", "https://bazel.build/query/guide", "https://git-scm.com/docs/git-sparse-checkout", "https://monorepo.tools/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monorepo build strategies

**Goal:** CI cost and time scale with the size of the *change*, not the size of the repo,
without ever skipping a test that the change could break.

(Tool overview and remote caching are in
`computing-software.devops-ci-cd.build-systems.fast-reproducible-cacheable-builds`.)

## 1. Affected detection must be correct before it is fast
"Affected" = projects whose files changed + everything that depends on them.
- **Base commit:** compare against the merge-base with the target branch, not `HEAD~1`:
  `nx affected -t test --base=origin/main --head=HEAD`,
  `turbo run test --filter='...[origin/main]'` (filter syntax changed across Turborepo
  majors — *verify*), Bazel: map changed files to targets then
  `bazel query "rdeps(//..., set($TARGETS))"` (or tools like `bazel-diff`/`target-determinator`).
- **Shallow clones break it.** CI checkouts default to depth 1; the base commit isn't
  there and tools fall back to "everything" or error. Use `fetch-depth: 0` or fetch the
  base explicitly (`git fetch --depth=100 origin main`), and on GitHub use
  `nrwl/nx-set-shas` or equivalent to find the last green main commit.
- On **main** itself, compare to the last *successful* main build, not the previous
  commit — otherwise a red build followed by a fix skips re-testing the broken projects.

## 2. Global inputs: the "everything is affected" trap
Some files affect all projects: root lockfile, root `tsconfig`, shared ESLint config,
CI scripts, toolchain versions. Declare them, or affected detection is wrong:
- Nx: `namedInputs` / `sharedGlobals` in `nx.json`.
- Turborepo: `globalDependencies` / `globalEnv` in `turbo.json`; task-level `env` for env vars.
- Bazel: they're just deps of the toolchain targets — make them explicit.
Then fight their blast radius: a root lockfile change shouldn't retest 300 packages if
only one package's deps moved. pnpm/Nx can hash per-project resolved deps from the lockfile
(*behaviour depends on version and config*); Bazel's per-package external repos achieve
the same.

## 3. Fan out in CI dynamically
Compute the affected list in a first job, emit a JSON matrix, and run one job per
project or per bucket:
```yaml
plan:
  outputs: { projects: ${{ steps.p.outputs.projects }} }
  steps:
    - run: echo "projects=$(npx nx show projects --affected --json)" >> "$GITHUB_OUTPUT"
      id: p
test:
  needs: plan
  if: needs.plan.outputs.projects != '[]'
  strategy: { matrix: { project: ${{ fromJSON(needs.plan.outputs.projects) }} } }
```
Hundreds of tiny jobs waste setup time — bucket small projects together. Keep one
always-present aggregate required check so empty matrices don't block merges.
Nx Cloud / Turborepo remote cache / Bazel remote execution offer distribution without
hand-built matrices.

## 4. Wire internal packages deliberately
- Workspaces (`pnpm`/`yarn`/`npm` workspaces with `workspace:*`, Gradle composite
  builds, Cargo workspaces, Go workspaces `go.work`).
- **Source vs built consumption:** importing a sibling's TypeScript source
  ("just-in-time" packages) means no build step but every consumer compiles it;
  importing built output means correct caching but an explicit `build` dependency
  (`dependsOn: ["^build"]` in Nx/Turbo). Pick one convention per repo.
- Versioning: fixed (all packages share one version) is simpler; independent versions
  need changesets or release-please manifests
  (`computing-software.devops-ci-cd.release-engineering.semantic-versioning-and-changelog-automation`).

## 5. Boundaries and ownership
- Enforce dependency rules: Nx `@nx/enforce-module-boundaries` with tags
  (`scope:payments`, `type:ui` cannot import `type:data-access`), Bazel `visibility`,
  `dependency-cruiser` or `import-linter` (Python). Without them the graph collapses
  into "everything depends on `utils`" and every change affects everything.
- CODEOWNERS per directory; required reviews per owner.
- Watch the dependency fan-in of shared libs; split hot `common` packages.

## 6. Scaling Git itself
At very large sizes: partial clone (`git clone --filter=blob:none`), sparse checkout
(`git sparse-checkout set apps/payments libs/shared`), `scalar` for maintenance and
filesystem monitor, and CI checkouts limited to needed paths where the build tool
allows. Keep large binaries out (Git LFS or an artifact store).

## Verify
- [ ] Changing a leaf library triggers exactly it + its dependents (compare with the graph tool's output).
- [ ] Changing a declared global input triggers the full set; nothing global is undeclared.
- [ ] CI uses a merge-base/last-green base and full enough history; shallow-clone fallback never silently runs "nothing".
- [ ] A full build of everything runs on main or nightly and is green.
- [ ] Boundary lint is required in CI and has no blanket ignores.
