---
id: computing-software.devops-ci-cd.build-systems.monorepo-project-graph-inspection
name: monorepo-project-graph-inspection
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, project-graph, nx-graph, affected, bazel-query, turbo-dry-run, dependency-graph]
level: practitioner
status: docs-checked
description: "Inspect and use a monorepo's project graph: nx graph and affected, turbo --dry and --filter, bazel query rdeps, pnpm workspace filters, and catching unwanted dependencies."
sources: ["https://github.com/nrwl/nx/tree/master/astro-docs/src/content/docs/features", "https://github.com/vercel/turborepo/blob/main/apps/docs/content/docs/reference/run.mdx", "https://pnpm.io/filtering", "https://bazel.build/query/language", "https://bazel.build/query/cquery"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Project graph inspection

The project graph (which package depends on which) drives everything a monorepo tool does: build order, caching, and "affected" CI. Inspecting it explains why CI ran 200 projects for a one-line change.

## Nx
```bash
npx nx graph                                    # interactive browser view
npx nx graph --focus=web-app --file=graph.json  # focus a project; --file exports the graph as JSON
npx nx show projects --affected -t build        # projects with an affected build task
npx nx affected -t lint test build --base=origin/main --head=HEAD
npx nx show project web-app --json              # one project's resolved configuration
```
Dependencies come from imports and package.json plus `implicitDependencies` (an array in project configuration). Enforce boundaries with project tags and the `@nx/enforce-module-boundaries` ESLint rule (`depConstraints`). `nx affected` selects tasks whose inputs your change touches; `--base` and `--head` set the compared commits (in CI, customise them).

## Turborepo
```bash
npx turbo run build --dry=json                      # task graph and what would run, as JSON
npx turbo run build --affected                      # by default equivalent to --filter=...[main...HEAD]
npx turbo run test --filter=...[origin/main]        # changed packages and their dependents
npx turbo run build --filter=...ui                  # ui and its dependents
npx turbo run build --graph=graph.svg               # graph file (the .png, .jpg, .pdf and .json formats are deprecated)
```

## pnpm workspaces
```bash
pnpm --filter "...foo" test                        # foo and everything that depends on it
pnpm --filter "...{packages/**}[origin/main]" test # changed projects under packages/ and their dependents
pnpm why lodash -r                                 # who depends on a package, recursively
pnpm ls -r --depth -1                              # workspace projects only
```

## Bazel
```bash
bazel query 'deps(//apps/web:server)' --output=graph > deps.dot   # render with Graphviz dot
bazel query 'rdeps(//..., //libs/auth:auth)'       # everything that depends on auth
bazel query 'somepath(//apps/web:server, //libs/legacy:db)'   # why does web depend on legacy db?
bazel cquery 'deps(//apps/web:server)' --output=files
```
Affected targets for a diff: the community tools `bazel-diff` and `target-determinator` compute changed targets between commits.

## Gradle / Maven
`./gradlew :app:dependencies --configuration runtimeClasspath`, `./gradlew projects`; Maven `mvn -pl module -amd` (`--also-make-dependents`) builds a module and the modules that depend on it.

## Using the graph
- "Why is everything affected?" - a root file (lockfile, tsconfig.base.json, shared config) is an input to every project; narrow the tool's input configuration or split shared config.
- Cycles: break them by extracting a shared interface package.
- Fan-in hotspots: libraries with hundreds of dependents make every change expensive; split them.
- Check the graph in CI (boundary lint, `bazel query` assertions in tests) so unwanted edges fail review.

## Verify
- [ ] For a change in one leaf library, the affected set contains only it and its dependents.
- [ ] Module boundary rules fail a PR that adds a forbidden dependency.

## Checked
Date: 2026-10-25. Documentation: Nx docs sources (nrwl/nx astro-docs: explore-graph, affected, enforce-module-boundaries), Turborepo docs (vercel/turborepo `reference/run.mdx`, `running-tasks.mdx`), pnpm docs (filtering, why, list), Bazel query docs (bazelbuild/bazel `docs/query/language.mdx`, `cquery.mdx`), Tinder/bazel-diff and bazel-contrib/target-determinator repositories.
Confirmed: `nx graph`, `--focus`, `--file`, `nx show projects --affected -t`, `nx affected --base/--head`, `implicitDependencies`, `@nx/enforce-module-boundaries` with `depConstraints`; turbo `--dry=json`, `--affected` default equivalence, `--filter=...[ref]` and `...pkg`, `--graph` formats; pnpm `...name`, `{dir}[since]` selectors, `why -r`, `ls --depth -1`; Bazel `deps`, `rdeps`, `somepath`, `--output=graph`, cquery `--output=files`; existence of bazel-diff and target-determinator.
Removed: `jq` post-processing examples, `--filter=web...` (replaced by the documented `...` forms), Gradle/Maven behaviour claims beyond the commands, the statement that Nx and Turborepo report cycles and that Bazel refuses to build them (not in the pages read), and `namedInputs`/`globalDependencies` specifics.
Method: documentation only; no commands were run.
