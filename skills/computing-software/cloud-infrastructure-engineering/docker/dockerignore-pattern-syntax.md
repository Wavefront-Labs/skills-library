---
id: computing-software.cloud-infrastructure-engineering.docker.dockerignore-pattern-syntax
name: dockerignore-pattern-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, dockerignore, dockerignore-patterns, dockerignore-negation, build-context, globstar, exclusion-rules, gitignore-vs-dockerignore]
level: practitioner
description: "Write .dockerignore patterns correctly: root-relative matching, ** globs, ! negation ordering, directory vs file semantics, and the ways it differs from .gitignore."
sources: ["https://docs.docker.com/build/concepts/context/#dockerignore-files", "https://github.com/moby/patternmatcher/tree/main/ignorefile", "https://docs.docker.com/reference/dockerfile/#buildkit-built-in-build-args"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# .dockerignore pattern syntax

**Goal:** a context that contains only what the build needs (no `.git`, `node_modules`,
secrets or large test fixtures) and no surprise where a needed file is missing.

## Matching rules
- The client looks for `.dockerignore` in the root directory of the context; matching files are
  removed from the context before it is sent to the builder.
- Patterns are relative to the **context root**. Leading and trailing slashes are disregarded:
  `/foo/bar/`, `/foo/bar`, `foo/bar/` and `foo/bar` all exclude `bar` in `foo`.
- Matching uses Go `filepath.Match` rules (`*`, `?`, `[...]`), after `filepath.Clean`
  preprocessing; blank lines are ignored and the pattern `.` is ignored. Docker adds `**`,
  which matches any number of directories (including zero): `**/*.go` excludes all `.go` files.
- `*/temp*` excludes names starting with `temp` in any immediate subdirectory of the root;
  `*/*/temp*` does so two levels down; `temp?` matches a one-character extension of `temp` in the
  root.
- A line starting with `#` in column 1 is a comment.
- `!pattern` makes an exception to an earlier exclusion. The **last line that matches** a file
  decides whether it is included or excluded, so order matters.
- Patterns stay relative to the context root even when the Dockerfile is elsewhere (`-f`).

## A starting point
```
# VCS and editor
.git
**/.DS_Store
.vscode
.idea
# dependencies and build output (rebuilt inside the image)
**/node_modules
**/__pycache__
.venv
dist
# secrets and local config
.env
.env.*
!.env.example
**/*.pem
# docker itself
Dockerfile*
docker-compose*.yml
.dockerignore
```
You can exclude the `Dockerfile` and `.dockerignore` themselves: they are still sent to the
builder because the build needs them, but you cannot copy them into the image with `ADD`,
`COPY` or bind mounts.

## Negation
```
*.md          # exclude markdown files right under the context root
!README.md    # except this one
```
Markdown files in subdirectories are not affected by `*.md`.
Order decides, as in the reference examples:
```
*.md
!README*.md
README-secret.md      # last match: README-secret.md is excluded
```
```
*.md
README-secret.md
!README*.md           # last match: all README files are included
```

## Gotchas
- A `.dockerignore` named after the Dockerfile (`<Dockerfile>.dockerignore`, next to it) takes
  precedence over the root one for that build.
- The ignore file keeps a build fast by not sending unwanted files, especially to a remote builder.
- If a build needs the version from `git describe`, a Git context can keep `.git` with
  `BUILDKIT_CONTEXT_KEEP_GIT_DIR`; otherwise pass the version as a `--build-arg`.
- Watch the "transferring context" line in the build output: a surprising size means the ignore
  file is wrong or missing.

## Verify
```sh
docker build --no-cache --progress=plain -f- . <<'EOF'
FROM busybox
COPY . /ctx
RUN find /ctx -maxdepth 2
EOF
```
lists exactly what reached the builder. The exact matching logic lives in the
moby/patternmatcher `ignorefile` package; do not assume `.gitignore` semantics.

## Checked

Checked 2026-10-23 against docker/docs "Build context" (.dockerignore files: filename and location, syntax, matching, negating matches).
Confirmed: location, slash handling, `filepath.Match` plus `**`, comment rule, `.` ignored, `!` last-match-wins examples, Dockerfile and `.dockerignore` still sent but not copyable, Dockerfile-specific ignore file precedence, `BUILDKIT_CONTEXT_KEEP_GIT_DIR`. Removed unconfirmed claims: that `!` cannot re-include inside an excluded directory, `.gitignore` difference list, `\` escaping, Compose and `--build-context` ignore-file behaviour.

Method: documentation only; no commands were run.
