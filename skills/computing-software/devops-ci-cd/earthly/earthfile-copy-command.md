---
id: computing-software.devops-ci-cd.earthly.earthfile-copy-command
name: earthfile-copy-command
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, copy, artifact-form, dir, keep-ts, keep-own, chmod, if-exists, symlink-no-follow]
level: practitioner
status: docs-checked
description: "Use Earthfile COPY in classical and artifact form, with --dir, --chmod, --keep-own, --if-exists, --symlink-no-follow, build-arg parentheses and glob targets."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# COPY in an Earthfile

Goal: copy files from the build context or from another target's artifacts.

Forms:
- `COPY [options...] <src>... <dest>` classical, from the build context
- `COPY [options...] <src-artifact>... <dest>` artifact form, e.g. `COPY +dummy-target/encoded-data .`
- `COPY [options...] (<src-artifact> --<build-arg-key>=<build-arg-value>...) <dest>`

Build args need parentheses: `COPY ( +dummy-target/encoded-data --encoder=base32 ) .`

Classical form differs from Dockerfile: URL sources are not supported, absolute source paths are not supported, and it behaves like `COPY --link`. Consecutive artifact COPYs build independent targets in parallel; copying happens in order. COPY does not mark the referenced target's images or pushes for output; use `BUILD`. Exclude files with `.earthlyignore`.

## Options
- `--dir`: copy the directories themselves, like `cp -r`. `COPY --dir dir1 dir2 dir3 ./` equals three COPYs in one layer. `COPY test .` and `COPY test/* .` copy contents; `COPY --dir test .` yields `./test/file`.
- `--keep-ts`: do not overwrite timestamps with a constant.
- `--keep-own`: keep ownership (artifact form only); the matching `SAVE ARTIFACT --keep-own` must be used.
- `--chmod <octal-format>`: e.g. `--chmod 0755` or `755`.
- `--if-exists`: ignore the COPY when the source is missing.
- `--symlink-no-follow`: copy a symlink from another target; use it in both `COPY` and `SAVE ARTIFACT`.
- `--platform`, `--allow-privileged`, `--pass-args` as for FROM. `--from` is not supported; use SAVE ARTIFACT plus artifact-form COPY.

## Glob targets (experimental)
`COPY ./services/*+mocks .` expands to each matching Earthfile defining `+mocks`; at least one match is required. Enable with `VERSION --wildcard-copy 0.8`. Wildcards in artifact names, such as `COPY ./services/service1+mocks/* .`, are fully supported.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
