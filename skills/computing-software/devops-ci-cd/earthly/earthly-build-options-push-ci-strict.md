---
id: computing-software.devops-ci-cd.earthly.earthly-build-options-push-ci-strict
name: earthly-build-options-push-ci-strict
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, push, no-output, no-cache, ci, strict, allow-privileged, interactive, secret]
level: practitioner
status: docs-checked
description: "Use earthly build options --push, --no-output, --no-cache, --ci, --strict, --platform, --allow-privileged, --secret and --interactive and their env var forms."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly build options

Goal: choose the right flag for pushing, CI, secrets and debugging. Each flag also has an env var form.

| Flag | Env var | Effect |
|---|---|---|
| `--push` | `EARTHLY_PUSH=true` | push images declared with push and run `RUN --push`; only in the output phase and only if the build succeeded |
| `--no-output` | `EARTHLY_NO_OUTPUT=true` | output no images or artifacts; not usable with artifact or image form |
| `--output` | `EARTHLY_OUTPUT=true` | allow output even under `--ci` |
| `--no-cache` | `EARTHLY_NO_CACHE=true` | ignore cache when building, but still store new cache |
| `--allow-privileged`, `-P` | `EARTHLY_ALLOW_PRIVILEGED=true` | permit `RUN --privileged` |
| `--interactive`, `-i` | `EARTHLY_INTERACTIVE=true` | on a failed `RUN`, drop into an interactive shell |
| `--strict` | none listed | disallow features that may create unrepeatable builds |
| `--ci` | `EARTHLY_CI=true` | target mode: alias for `--no-output --strict`; artifact and image modes: alias for `--strict` |
| `--platform <platform>` | `EARTHLY_PLATFORMS=<platform>` | platform to build for |
| `--secret`, `-s <id>[=<value>]` | `EARTHLY_SECRETS="id=value,..."` | pass a secret; without a value, the env var of the same name is used |
| `--secret-file <id>=<path>` | `EARTHLY_SECRET_FILES` | load a file into a secret |
| `--auto-skip` (experimental) | `EARTHLY_AUTO_SKIP=true` | skip targets unchanged since a previous build |

Secrets are used in recipes as `RUN --secret <env-var-name>=<secret-id>`, and can also live in a `.secret` file with the same syntax as `.arg`.

## Multiple platforms
`--platform` takes one platform. For several, use a wrapping target:
```
build-all-platforms:
  BUILD --platform=linux/amd64 --platform=linux/arm/v7 +build
```

## Gotcha
Only one interactive shell can be used on the system at a time.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthly-command/earthly-command.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
