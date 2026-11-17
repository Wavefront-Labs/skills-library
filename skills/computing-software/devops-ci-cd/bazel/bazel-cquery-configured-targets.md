---
id: computing-software.devops-ci-cd.bazel.bazel-cquery-configured-targets
name: bazel-cquery-configured-targets
category: computing-software
field: devops-ci-cd
product: bazel
tags: [bazel-cquery, configured-targets, universe-scope, select, config-function, exec-configuration, bazel-config]
level: advanced
status: docs-checked
description: "Use cquery to resolve select() and configurations, set --universe_scope, and read configuration hashes."
sources: ["https://bazel.build/query/cquery"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# bazel cquery

`cquery` runs over the analysis-phase configured target graph, so it applies command-line build options and picks the real `select()` branch. Plain `query` conservatively lists every branch.

```bash
bazel query  "deps(//tree:ash)" --noimplicit_deps                      # all branches
bazel cquery "deps(//tree:ash)" --define species=excelsior --noimplicit_deps
```

Results look like `//tree:ash (9f87702)`: the suffix is a prefix of the configuration's SHA-256. `bazel config 9f87702` prints its contents; plain `bazel config` lists full IDs. `(exec)` also appears for exec-configured targets.

A pattern like `//foo` matches every configured version of `//foo`, so you may get two lines (target and exec configuration). Use `--universe_scope=//x:my_gen` to query a target as a dependency of another, for example a genrule tool lands in the exec configuration. Set it whenever the expression is more complex than `deps(//foo)`; it also prevents building in configurations you do not care about.

New function: `config(expr, hash)` selects a configured target by configuration (`null` or a hash).

Flags: `--[no]implicit_deps` (also hides resolved toolchains), `--[no]tool_deps`, `--[no]include_aspects`. Not supported: `allrdeps`, `buildfiles`, `loadfiles`, `rbuildfiles`, `siblings`, `tests`, `visible`; `test_suite` is not a configured target.

cquery cannot see actions; use aquery for that (see bazel-aquery-action-graph).

## Checked

2026-11-04. Read against the Bazel docs page(s): Query / cquery pages (cquery reference and guide) (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the closing Verify line.
Method: documentation only; no commands were run.
