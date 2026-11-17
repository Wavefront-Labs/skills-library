---
id: computing-software.devops-ci-cd.gitlab-ci.pipeline-templates-and-includes
name: pipeline-templates-and-includes
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, gitlab, include, include-project, include-local, include-remote, include-template, include-component, ci-cd-components, ci-catalog, spec-inputs, inputs, extends, hidden-jobs, yaml-anchors, reference-tag, merged-yaml, pipeline-editor, central-templates, shared-ci, platform-team, versioning, compliance-pipelines, pipeline-execution-policy]
level: advanced
status: docs-checked
description: "Share GitLab CI config across projects: include types, CI/CD components with spec:inputs, extends vs !reference vs anchors, merge semantics, versioning and the merged-YAML check."
sources: ["https://docs.gitlab.com/ci/yaml/includes/", "https://docs.gitlab.com/ci/components/", "https://docs.gitlab.com/ci/yaml/#specinputs", "https://docs.gitlab.com/ci/yaml/yaml_optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline templates and includes

**Goal:** a platform team maintains CI once; hundreds of projects consume it with a
version pin and a few inputs, and nobody has to guess what the merged pipeline looks like.

## 1. The include types
```yaml
include:
  - local: .gitlab/ci/test.yml                   # same repo, same ref
  - project: platform/ci-templates               # another project
    ref: v3.2.0                                  # tag/SHA — never a moving branch for prod
    file: [/templates/build.yml, /templates/scan.yml]
  - remote: https://<host>/ci/shared.yml         # fetched over HTTP; no auth, avoid
  - template: Jobs/SAST.gitlab-ci.yml            # GitLab-shipped templates
  - component: $CI_SERVER_FQDN/platform/components/node-ci@1.4.0
    inputs: { node_version: "22", stage: test }
```
- Includes are resolved when the pipeline is created. Nested includes run without user context, so they can only include public projects or templates.
- Up to 150 includes per pipeline by default, including nested ones; self-managed instances can change the maximum.
- `include:rules` with `if:` lets you include files conditionally (only certain variables are available there; see the include docs).

## 2. CI/CD components (current recommended unit)
```yaml
spec:
  inputs:
    stage: { default: test }
    node_version: { default: "22" }
    run_lint: { type: boolean, default: true }
---
"$[[ inputs.stage ]]-node-test":
  stage: $[[ inputs.stage ]]
  image: node:$[[ inputs.node_version ]]
  script: [npm ci, npm test]
```
- Inputs are interpolated with `$[[ inputs.x ]]` at include time, are typed (`string`,
  `number`, `boolean`, `array`), and support `regex:` validation — far safer
  than "set this variable and hope".
- Released component versions can be listed in the **CI/CD Catalog**. Consumers can pin a full version (`@1.4.0`), a partial version such as `@1.4` (latest matching), `@~latest`, or a SHA.
- Prefix job names with an input or component name to avoid collisions between components.

## 3. Reuse inside YAML: extends vs !reference vs anchors
- **`extends:`** — deep-merges hashes from a (usually hidden, `.dot`-prefixed) job, works
  across included files. Arrays are **replaced**, not concatenated: extending a job and
  setting `script:` overwrites the parent's script entirely.
- **`!reference [.setup, script]`** — pull one key (or a list) from another job, *across
  files*; can be spliced into arrays:
  `script: [!reference [.setup, script], npm test]`.
- **YAML anchors** (`&base` / `<<: *base`) — plain YAML; prefer `extends`/`!reference` for config that crosses included files.

## 4. Merge semantics (where surprises come from)
- Same job name in the consumer and an include → keys deep-merge, consumer wins. That's
  the override mechanism: redefine `sast: { rules: [{ when: never }] }` to disable a template job.
- When keys overlap between included files, the last included file takes precedence, and the main file wins over included files.

## 5. Enforcement, not just sharing
Includes are opt-in: a project can delete them. For mandatory scans, use
**pipeline execution policies** / compliance frameworks (Ultimate tier; the older
"compliance pipelines" feature is deprecated) — check what your tier and version offer.

## 6. Seeing the result
The pipeline editor and the CI Lint tool validate the configuration with includes resolved. Always review the merged result after a template bump.

## Verify
- [ ] Every cross-project include/component is pinned to a tag or SHA.
- [ ] Components use typed `spec:inputs` instead of magic variables.
- [ ] No consumer relies on YAML anchors defined in another file.
- [ ] Overrides in consumers are deliberate and visible in the merged YAML.
- [ ] Template repo has its own pipeline that includes the components and runs them on each MR.

## Checked

2026-10-28. Confirmed on the includes, components, CI YAML and YAML optimization pages: include types, 150 includes per pipeline (self-managed adjustable), nested includes run as a public user, spec:inputs with $[[ inputs.x ]] interpolation, input types string/number/boolean/array, regex validation, component versions @1.0.0, partial @1.0 and @~latest, the CI/CD Catalog, extends merging hashes but not arrays, !reference, the merge method for include, Ultimate pipeline execution policies and the deprecated compliance pipelines. Removed: component folder layout, input options, @1 shorthand, release-job detail, anchor and stages/default merge claims, CI Lint API call, Full configuration view name. Sources updated to current URLs; the inputs page returned a sign-in redirect so it was replaced with the CI YAML spec:inputs section. Versions v3.2.0 and 1.4.0 are example placeholders.
Method: documentation only; no commands were run.
