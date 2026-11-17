---
id: computing-software.devops-ci-cd.gitlab-ci.extends-and-include-merge-rules
name: extends-and-include-merge-rules
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, extends-merge, include-merge-behavior, extends, include]
level: advanced
status: docs-checked
description: "Predict how extends and include merge GitLab CI config: hashes deep-merge, arrays replace, later files win, and how to append to script or variables safely."
sources: ["https://docs.gitlab.com/ci/yaml/yaml_optimization/#merge-details", "https://docs.gitlab.com/ci/yaml/includes/#merge-method-for-include"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# extends and include merge rules

## The rule
- **Hashes deep-merge**; `extends` merges hashes but not arrays.
- **Arrays are not merged**: the docs show `tags: [postgres]` overwriting `tags: [dev]`, and the example below replaces `script`.
- Later wins: for `extends: [.a, .b]`, `.b` overrides `.a`; the job's own keys override both.
- For `include`, the including file wins over included files; among includes, later entries win.

```yaml
.base:
  variables: { A: "1", B: "1" }
  script: [echo base]
  tags: [docker]
job:
  extends: .base
  variables: { B: "2" }      # result A=1, B=2
  script: [echo job]         # result: only "echo job"
```

## Appending instead of replacing
Use `!reference` to splice arrays:
```yaml
job:
  extends: .base
  script:
    - !reference [.base, script]
    - echo extra
```
`!reference` tags nest up to 10 levels deep in `script`, `before_script` and `after_script`.

## Unsetting
To exclude a key from the extended content, assign it `null` (the docs example `variables: null`); an empty hash (`variables: {}`) keeps the inherited variables.

## YAML anchors vs extends
Anchors (`<<: *x`) are resolved by the YAML parser; `extends` deep-merges hashes and works together with `include`, so prefer it.

## Debugging
Use the CI Lint tool or the pipeline editor to check the merged result; compare before and after when refactoring templates.

## Verify
- [ ] Merged YAML shows the expected script and variables for each job.

## Checked

2026-10-28. Confirmed on the YAML optimization and includes pages: extends performs a reverse deep merge on keys and merges hashes but not arrays, the last extended member overrides others, null excludes a key (variables: null) while variables: {} keeps inherited values, !reference nests up to 10 levels in script sections, extends works with include, include merge order (last included file wins, main file merged over includes). Removed: the garbled list of keys, cross-file !reference claim, the Full configuration view and glab ci config compile.
Method: documentation only; no commands were run.
