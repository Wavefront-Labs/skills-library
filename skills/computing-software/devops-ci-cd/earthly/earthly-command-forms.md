---
id: computing-software.devops-ci-cd.earthly.earthly-command-forms
name: earthly-command-forms
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, target-ref, artifact, image, build-phases, local-reference, remote-reference]
level: intro
status: docs-checked
description: "Run an Earthly build in target, artifact or image form, with local or remote target references, and know its four phases: init, build, push, local output."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly command forms and target references

Goal: pick the right `earthly` invocation form and write a correct target or artifact reference.

## Forms
```
earthly [options...] <target-ref> [build-args...]
earthly [options...] --artifact|-a <target-ref>/<artifact-path> [<dest-path>] [build-args...]
earthly [options...] --image <target-ref> [build-args...]
```
- Target form builds the target and its dependencies.
- Artifact form builds them but outputs only the named artifact; `<dest-path>` optionally overrides where it goes.
- Image form builds them but outputs only the specified image.

If no BuildKit daemon is running and `--buildkit-host` is not given, the command starts a container named `earthly-buildkitd` as the build daemon.

## References
- `+<target-name>`: target in the Earthfile in the current directory.
- `<local-path>+<target-name>`: Earthfile in another directory; `<local-path>` must start with `./`, `../` or `/`.
- `<gitvendor>/<namespace>/<project>/path/in/project[:some-tag]+<target-name>`: remote git repository.
- `<target-ref>/<artifact-path>`: an artifact built by a target.

## Phases
1. Init: configuration is interpreted and the BuildKit daemon started if applicable.
2. Build: the target and all direct and indirect dependencies run.
3. Push (optional, off by default): image pushes and `RUN --push` commands.
4. Local output (optional, on by default): artifacts with `AS LOCAL` are written out and docker images are loaded onto the host docker daemon.

## Gotcha
If the build phase fails, no output is produced and no push instruction runs; the command exits non-zero.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthly-command/earthly-command.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
