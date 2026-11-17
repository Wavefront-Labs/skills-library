---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-cel-when-expressions
name: tekton-pipeline-cel-when-expressions
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, cel, when, alpha]
level: advanced
status: docs-checked
description: "Write CEL expressions in Tekton when blocks for numeric comparison, logic operators and regex matching, with the single-quote substitution rule."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CEL in `when` is alpha: set `enable-cel-in-whenexpression` to `"true"`. A `cel` string replaces the `input`/`operator`/`values` triple and must evaluate to true or false.

```yaml
when:
  - cel: "'foo' in ['foo', 'bar']"
  - cel: "!('duh' in ['foo', 'bar'])"
  # numeric, logic and regex forms
  - cel: "'$(tasks.unit-test.results.test-coverage)' > 0.9"
  - cel: "'$(params.param1)' != '' || '$(params.param2)' == '8.5'"
  - cel: "'$(params.branch)'.matches('release/.*')"
```

Variable substitution works for string params/results, array indexing (`$(params.branch[0])`) and object keys (`$(params.repo.url)`), but references must be wrapped in single quotes, so that `'$(params.foo)' == 'foo'` is valid while `$(params.foo) == 'foo'` is not and bare `params.foo == 'foo'` is unsupported. Because substitution is done by string replacement, a CEL expression passed in through a param or result is not executed, which prevents CEL injection.

Whole array or object replacement (`'$(params.array_params[*])'`) is not supported. Expressions are validated by the admission webhook, which rejects invalid CEL.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
