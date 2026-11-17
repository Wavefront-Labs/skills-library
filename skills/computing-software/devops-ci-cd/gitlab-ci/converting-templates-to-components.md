---
id: computing-software.devops-ci-cd.gitlab-ci.converting-templates-to-components
name: converting-templates-to-components
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, template-to-component, include-template-migration, component-refactor]
level: advanced
status: docs-checked
description: "Migrate legacy include templates to CI/CD components: move into templates/, replace variables with inputs, remove global keywords, unique job names, and roll out to consumers."
sources: ["https://docs.gitlab.com/ci/components/#convert-a-cicd-template-to-a-component", "https://docs.gitlab.com/ci/inputs/", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/components/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting templates to components

## 1. Steps
1. Copy the template into `templates/build.yml` in a component project (new or existing).
2. Replace configuration-by-variable with **inputs**:
```yaml
# before (template)
variables: { BUILD_IMAGE: node:20-alpine, BUILD_STAGE: build }
build: { stage: $BUILD_STAGE, image: $BUILD_IMAGE, script: npm run build }

# after (component)
spec:
  inputs:
    image: { default: "node:22-alpine" }
    stage: { default: build }
    job-name: { default: build }
---
"$[[ inputs.job-name ]]":
  stage: $[[ inputs.stage ]]
  image: $[[ inputs.image ]]
  script: npm run build
```
3. Avoid global keywords in the component: they affect every job in the consuming pipeline. Put the configuration on each job, or use `extends` with unique names. Use an input for `stage` rather than hardcoding it.
4. Prefer inputs to hardcoded values; keep a hidden job only if consumers intentionally extend it (document it).
5. Keep the old template as a thin wrapper during migration:
```yaml
# old path, kept for compatibility
include:
  - component: $CI_SERVER_FQDN/platform/ci/build@1
    inputs: { image: $BUILD_IMAGE }
```
   (inputs can use CI/CD variables but with the same limitations as variables in `include`; use `expand_vars` to expand a variable inside an input, and note environment-scoped variables are not available to it).
6. Test the component in the project's `.gitlab-ci.yml`, tag and release it (semantic version, `release` keyword), then deprecate the template path.

## 2. Gotchas
- Variables that consumers set at project level (`BUILD_IMAGE`) silently stop mattering once
  inputs take over — grep consumers before removing.
- Job names change if you add prefixes, so any consumer `needs` that name the old job break.
- Only the `template.yml` file of a component directory is used by consumers; other files are not released with the component.

## Verify
- [ ] A consumer's full configuration is identical (jobs/stages/images) before and after switching.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/components/_index.md: the documented conversion steps (copy into the component directory structure, refactor following the writing guidance, test in the component repo's pipeline, tag and release), the advice to avoid global keywords and hardcoded `stage`, `expand_vars` and variable limitations in doc/ci/inputs/_index.md, and `template.yml`-only release. The thin-wrapper migration pattern is the skill's own suggestion built from documented `include:component` and `inputs` syntax. Removed the claims about job-name and rules limits and about required status checks.

Method: documentation only; no commands were run.
