---
id: computing-software.devops-ci-cd.bazel.bazel-aquery-action-graph
name: bazel-aquery-action-graph
category: computing-software
field: devops-ci-cd
product: bazel
tags: [bazel-aquery, action-graph, mnemonic, skyframe-state, output-commands, inputs-outputs-filter]
level: advanced
status: docs-checked
description: "Inspect the real actions, command lines and inputs Bazel will run with aquery filters and output formats."
sources: ["https://bazel.build/query/aquery"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# bazel aquery

`aquery` works on the post-analysis action graph: actual command lines, inputs, outputs and mnemonics. It inherits all build options and supports query functions except `siblings`, `buildfiles` and `tests`.

```bash
bazel aquery 'deps(//src/target_a)'
bazel aquery 'inputs(".*cpp", deps(//src/target_a))'
bazel aquery 'mnemonic("Cpp.*", inputs(".*cpp", inputs("foo.*", //src/target_a)))'   # AND
bazel aquery --output=commands //src/target_a                  # one command per line
bazel aquery --output=jsonproto 'outputs("foo.out", //target_a)'
```

Three aquery-only filters: `inputs(regex, expr)`, `outputs(regex, expr)`, `mnemonic(regex, expr)`. They produce actions, so they cannot be nested inside non-aquery functions: `deps(inputs(...))` is a syntax error. Combine them by nesting the filters themselves.

Output: `--output=text|summary|commands|proto|jsonproto|textproto`; proto message is `analysis.ActionGraphContainer`. Trim big output with `--noinclude_commandline`, `--noinclude_artifacts`; add `--include_param_files` (which forces command lines on) or `--include_file_write_contents`.

Find which target made a file without re-analysis: `bazel aquery --output=proto --skyframe_state 'outputs("foo.out")'` dumps the action graph Skyframe still holds in the running server. It works only with proto or textproto output, and giving a target label together with `--skyframe_state` is a syntax error.

## Checked

2026-11-04. Read against the Bazel docs page(s): Action Graph Query (aquery) (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the generic closing Verify line.
Method: documentation only; no commands were run.
