---
id: computing-software.devops-ci-cd.concourse-ci.across-step-modifier
name: across-step-modifier
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [across, matrix, max-in-flight, fail-fast, load-var, dynamic-steps, build-matrix]
level: advanced
status: docs-checked
description: "Fan a step out over combinations of values with across: var/values, multiplicative combinations, max_in_flight all or N, fail_fast, and dynamic lists loaded with load_var."
sources:
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/across/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`across` runs a step repeatedly for every combination of variable values. Each `across_var` has `var` and `values`; the var is a local var `((.:name))` scoped to that iteration. A warning is printed if a parent-scope var has the same name. Outputs from steps inside an across are not available outside it.

```yaml
plan:
  - get: foo
  - load_var: packages
    file: foo/packages-to-build.json
  - across:
      - var: package
        values: ((.:packages))
      - var: go_version
        values: [ '1.15', '1.16' ]
    task: build
    file: foo/build.yml
    vars:
      go_version: ((.:go_version))
      package: ((.:package))
```

With a JSON array of three packages and two Go versions, six iterations run. `values` can be interpolated, so a `load_var` step can supply a dynamic list.

`max_in_flight` on a var (default `1`) is `all` or a number. With several vars the effective parallelism is multiplicative: var1 with `all` over 3 values, var2 default 1 over 2 values and var3 limited to 2 gives 6 substeps in parallel. `fail_fast` (default `false`, at the same level as `across`) stops as soon as any substep fails.

Use `do` to repeat several steps per value. Combined with `set_pipeline` and `instance_vars`, across maintains a dynamically sized group of pipelines.

## Checked

2026-11-04. Var semantics, max_in_flight multiplication, fail_fast and examples confirmed on the Across Step Modifier page.

Method: documentation only; no commands were run.
