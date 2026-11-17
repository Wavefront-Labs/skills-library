---
id: computing-software.devops-ci-cd.concourse-ci.implementing-resource-types
name: implementing-resource-types
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [resource-types, check, in, out, opt-resource, json, metadata, stdin]
level: advanced
status: docs-checked
description: "Build a custom resource type: an image with /opt/resource/check, in and out scripts, their stdin JSON, version ordering, output and metadata, with the git resource as example."
sources:
  - https://concourse-ci.org/docs/resource-types/implementing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A resource type is a container image with three executables:
- `/opt/resource/check`: detect new versions
- `/opt/resource/in`: pull a version down
- `/opt/resource/out`: idempotently push a version up

All three must exist, though they can be no-ops. Packaging as an image lets a type carry its own dependencies, such as the git binary. Logs go to `stderr`, and ANSI escape codes are rendered by the web UI.

**check** receives `{"source": {...}, "version": {...}}` on stdin (version is an object of string fields, like the git `ref`). It prints a JSON array of versions in chronological order, oldest first, including the requested version if still valid. The array may be empty if none exist. If the given version is already the latest, return it as the sole entry. If versions cannot be ordered (for example a git commit that was force-pushed over), return the current version. The check container is reused between checks, so a git check can conditionally clone and then pull.

**in** gets the destination directory as `$1`, and on stdin `source`, an exact `version`, and `params` (from the `get` step). It must place the resource in that directory and exit with an error if the version no longer exists. It prints `{"version": {...}, "metadata": [{"name": "commit", "value": "61cebf"}]}`; metadata is public and shown on the build page.

**out** gets the directory holding all build sources as `$1` and on stdin `source` and `params` (from the `put` step). It prints the resulting version, such as the pushed commit SHA, plus optional metadata.

## Checked

2026-11-04. Script contract, request and response shapes confirmed on the Implementing a Resource Type page (check, in and the beginning of out); the whole page was read; its Build Metadata, certificate propagation and local docker testing sections are not covered here.

Method: documentation only; no commands were run.
