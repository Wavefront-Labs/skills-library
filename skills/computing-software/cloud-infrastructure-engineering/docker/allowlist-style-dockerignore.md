---
id: computing-software.cloud-infrastructure-engineering.docker.allowlist-style-dockerignore
name: allowlist-style-dockerignore
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerignore, dockerignore-allowlist, build-context, dockerignore-negation, context-size]
level: practitioner
status: docs-checked
description: "Write a deny-all .dockerignore (* then ! exceptions) so only listed files reach the builder; ordering rules, nested re-excludes and how to test what gets sent."
sources: ["https://docs.docker.com/build/concepts/context/#dockerignore-files", "https://github.com/moby/patternmatcher/tree/main/ignorefile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Allowlist-style .dockerignore

A denylist grows forever and leaks the next new secret file. An allowlist sends only what the
Dockerfile copies.

## Template
```gitignore
# deny everything
*

# allow what the build needs
!package.json
!package-lock.json
!tsconfig.json
!src

# re-exclude junk that lives inside allowed directories (later lines win)
**/node_modules
**/.DS_Store
```

## Rules that matter
- The last line of `.dockerignore` that matches a file decides whether it is included or
  excluded. Put `*` first, exceptions after, re-excludes last.
- Patterns are relative to the context root; `**` matches any number of directories.
- The `Dockerfile` and `.dockerignore` can be excluded; they are still sent to the builder
  because the build needs them (they cannot be copied into the image).
- A Dockerfile-specific ignore file (`<Dockerfile>.dockerignore`) takes precedence over the root
  file for that build, so it must contain the complete allowlist.

## Testing what is sent
```bash
docker build -f- . <<'EOF'
FROM busybox
COPY . /ctx
RUN find /ctx -type f
EOF
```
Run with `--progress=plain` to see the file list, and watch the "transferring context" size.

## Gotchas
- `COPY . .` with an allowlist silently omits a newly added top-level folder, so the failure shows
  up late; add a smoke test.
- With several Dockerfiles in one repository, use one allowlist per Dockerfile
  (`<Dockerfile>.dockerignore`) or build from a narrower context.
- Only the `.dockerignore` for the build context applies (or the Dockerfile-specific one), not a
  file next to a Compose file.

## Checked

Checked 2026-10-23 against docker/docs "Build context" (.dockerignore syntax, negating matches, Dockerfile and `.dockerignore` handling, Dockerfile-specific ignore files).
Confirmed: last-match-wins semantics, `**`, context-root-relative patterns, Dockerfile and `.dockerignore` still sent to the builder, per-Dockerfile ignore precedence. Removed unconfirmed claims: that `!src/` versus `!src/**` differ, the legacy-builder `!Dockerfile` requirement and the Compose location remark.

Method: documentation only; no commands were run.
