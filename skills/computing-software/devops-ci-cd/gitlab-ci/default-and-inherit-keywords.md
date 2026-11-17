---
id: computing-software.devops-ci-cd.gitlab-ci.default-and-inherit-keywords
name: default-and-inherit-keywords
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, default-keyword, inherit-default, inherit-variables, global-defaults]
level: practitioner
status: docs-checked
description: "Set pipeline-wide job defaults with the default keyword and opt individual jobs out with inherit:default and inherit:variables, replacing deprecated top-level globals."
sources: ["https://docs.gitlab.com/ci/yaml/#default", "https://docs.gitlab.com/ci/yaml/#inherit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `default` and `inherit`

## 1. default
```yaml
default:
  image: node:22-alpine
  tags: [docker]
  interruptible: true
  retry: { max: 2, when: [runner_system_failure] }
  before_script: [npm ci --prefer-offline]
  cache: { key: { files: [package-lock.json] }, paths: [.npm/] }
variables:
  NPM_CONFIG_CACHE: $CI_PROJECT_DIR/.npm
```
Keywords allowed in `default`: `after_script`, `artifacts`, `before_script`, `cache`, `hooks`,
`id_tokens`, `image`, `interruptible`, `retry`, `services`, `tags`.
A job keyword **replaces** (does not merge) the default for that keyword — a job with its own
`cache:` loses the default cache entirely.
Top-level `image:`, `services:`, `cache:`, `before_script:`, `after_script:` are deprecated
globals — move them under `default:`.

## 2. inherit
```yaml
deploy-docs:
  inherit:
    default: false                      # ignore every default
    variables: false                    # ignore every top-level variable
  image: alpine
  script: ./publish.sh

trigger-child:
  inherit:
    default: [retry, tags]              # keep only these defaults
    variables: [ENVIRONMENT]            # pass only this global variable
  trigger: { include: child.yml }
```
`inherit:variables` matters for `trigger:` jobs: variables a trigger job inherits are passed to
downstream pipelines, so list only the ones the child needs. Global `default:` keywords are not
passed downstream.

## 3. Gotchas
- `inherit:default` and `inherit:variables` each take `true` (the default), `false`, or a list of names to keep.
- Global defaults are not passed to downstream pipelines, which run independently.

## Verify
- [ ] The opted-out job's log shows no default `before_script` lines.

## Checked

2026-10-31. Confirmed against the GitLab CI YAML reference: the list of keywords that can have defaults (after_script, artifacts, before_script, cache, hooks, id_tokens, image, interruptible, retry, services, tags), job keyword takes precedence without merging, inherit:default and inherit:variables values (true default, false, list), deprecation of top-level image, services, cache, before_script and after_script outside default, trigger yaml_variables passing, global defaults not passed downstream, and the retry when values.
Removed: `timeout` as a default keyword (not in the list), `stuck_or_timeout_failure` (deprecated in the docs), the `before_script: []` claim, the include-merge, hidden-job and extends gotchas, and the pipeline-editor verify step.

Method: documentation only; no commands were run.
