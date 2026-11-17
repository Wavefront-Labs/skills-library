---
id: computing-software.devops-ci-cd.gitlab-ci.component-inputs-types-defaults-and-regex
name: component-inputs-types-defaults-and-regex
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, inputs-types, inputs-default, inputs-regex, spec-inputs, inputs-interpolation]
level: advanced
status: docs-checked
description: "Define spec:inputs for CI components and includes: types (string, number, boolean, array), defaults, options, regex validation, descriptions and interpolation functions."
sources: ["https://docs.gitlab.com/ci/inputs/", "https://docs.gitlab.com/ci/yaml/#specinputs", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/inputs/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# spec:inputs: types, defaults, regex

## 1. Header (separated from the body by `---`)
```yaml
spec:
  inputs:
    stage:
      default: test
    job-prefix:
      default: ""
      description: Prefix to make job names unique when included twice
    python-version:
      options: ["3.11", "3.12", "3.13"]
      default: "3.12"
    coverage-min:
      type: number
      default: 80
    run-lint:
      type: boolean
      default: true
    extra-args:
      type: array
      default: []
    image-tag:
      regex: ^v\d+\.\d+\.\d+$          # validated at pipeline creation
---
"$[[ inputs.job-prefix ]]pytest":
  stage: $[[ inputs.stage ]]
  image: python:$[[ inputs.python-version ]]
  script:
    - echo "coverage minimum $[[ inputs.coverage-min ]]"
    - echo "run-lint is $[[ inputs.run-lint ]]"
  rules:
    - if: '"$[[ inputs.run-lint ]]" == "true"'
```

## 2. Rules
- No `default` means the input is mandatory; a `default` makes it optional. Always set defaults for inputs used by pipelines not created through `include`, or automatically triggered pipelines can fail to start.
- Types: `string` (default when `type` is omitted), `number`, `boolean`, `array`. Inputs are validated at pipeline creation.
- `options` lists the allowed values; `regex` must match and can only be used with `type: string`.
- Interpolation `$[[ inputs.x ]]` happens when the pipeline is created, not when jobs run. An input that replaces a whole YAML value is interpolated as its type; inside a string it is always text. Array input inside a string becomes its string representation.
- Functions go inside the block: `$[[ inputs.x | expand_vars ]]` (expand CI/CD variables in the value), `truncate(offset,length)`, `posix_escape` (GitLab 18.6; not a security control for untrusted values; put `expand_vars` first when combined). At most 3 functions per block.
- Limits: an interpolation block must be under 1 KB, a string that uses an input under 1 MB.

## 3. Passing inputs
```yaml
include:
  - component: $CI_SERVER_FQDN/platform/python/pytest@1.4.0
    inputs:
      stage: verify
      coverage-min: 90
      extra-args: ["-n", "auto"]
```
`include:inputs` works for any configuration added with `include` that has a `spec` header; downstream pipelines use `trigger:inputs`. Array inputs given through the trigger API or push options must be JSON, for example `["a", "b"]`.

## Gotchas
- Inputs are not CI/CD variables. They are substituted into the configuration at pipeline creation, so do not pass secrets as inputs; keep them in masked or protected CI/CD variables.
- Included configuration merges into the pipeline by name: two jobs with the same name merge into one, so give a component a job-name or prefix input if it may be included twice.

## Verify
- [ ] Passing an `image-tag` that does not match the regex fails pipeline creation.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/components/_index.md and doc/ci/inputs/_index.md plus doc/ci/yaml/_index.md: `spec:inputs` keywords (`default`, `options`, `regex`, `type`, `description`), the four types, mandatory-without-default, regex only for strings, interpolation functions (`expand_vars`, `truncate(offset,length)`, `posix_escape` from 18.6), the limit of three functions per block, the 1 KB and 1 MB limits, and `trigger:inputs`. Removed the claims that `$[[ ]]` inside `script` stays literal (the docs show it interpolated), that interpolation precedes variables entirely, and the pytest flags (third-party tool).

Method: documentation only; no commands were run.
