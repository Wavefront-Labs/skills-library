---
id: computing-software.devops-ci-cd.bazel.bazel-query-dependency-recipes
name: bazel-query-dependency-recipes
category: computing-software
field: devops-ci-cd
product: bazel
tags: [bazel-query, deps, rdeps, somepath, allpaths, kind, attr, buildfiles, output-graph]
level: practitioner
status: docs-checked
description: "Answer dependency questions with bazel query: deps, rdeps, somepath, allpaths, kind and attr filters, and graph output."
sources: ["https://bazel.build/query/guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# bazel query recipes

`bazel query` runs over the loading-phase graph, before options and `select()` are evaluated. Add `--keep_going` to ignore missing targets.

```bash
bazel query "deps(//foo)"                       # everything needed to build //foo
bazel query "rdeps(//..., //foo:lib)"           # what breaks if //foo:lib changes
bazel query "somepath(//foo:foo, third_party/zlib:zlibonly)"   # one chain
bazel query "allpaths(//foo, third_party/...)" --notool_deps --output graph | dot -Tsvg > deps.svg
bazel query "deps(//foo) except deps(//foo:foolib)"
```

Useful flags: `--notool_deps` drops tooling dependencies; `--noimplicit_deps` drops dependencies added by rules (for example the proto compiler for a genproto rule).

Filters and listings:
```bash
bazel query 'foo/...' --output package                     # packages under foo
bazel query 'kind(rule, foo:*)' --output label_kind
bazel query 'kind("generated file", //foo:*)'
bazel query 'tests(//foo:smoke_tests)'                     # expand a test_suite
bazel query 'attr(size, small, tests(//foo:smoke_tests))'
bazel query 'kind(".*_test rule", //foo/...)'
bazel query path/to/file.java                              # label for a file
bazel query 'buildfiles(deps(//foo:foo))' --output package # packages to check out
bazel query 'some(kind(cc_.*library, deps(//foo)))' --output location
```

`kind` and `filter` take regular expressions. Use `let x = ... in ...` with `$x` to reuse a set. `rdeps(u, x)` searches only inside the universe `u`; Sky Query adds `allrdeps` for a chosen universe.

## Checked

2026-11-04. Read against the Bazel docs page(s): Query how-to guide and cquery reference (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the closing Verify line.
Method: documentation only; no commands were run.
