---
id: computing-software.devops-ci-cd.skaffold.file-sync-manual-infer
name: file-sync-manual-infer
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [sync, manual, infer, hot-reload]
level: advanced
status: docs-checked
description: "Copy changed files into running containers instead of rebuilding, using manual rules or inferred ones from the Dockerfile."
sources:
  - "https://skaffold.dev/docs/filesync/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

File sync copies changed files into running containers instead of rebuilding, redeploying and restarting the pod. Skaffold tars the changed files that match the sync rules and extracts them in the container. Configure it per artifact under `sync`.

Manual mode (supported by every artifact type):

```yaml
artifacts:
- image: app
  sync:
    manual:
    - src: "static-html/*.html"
      dest: static
    - src: "content/en/**/*.md"
      dest: content
      strip: content/en/
```

- `src` and `dest` are required. `src` is a glob relative to the artifact `context`, and can use `**` for nested files; directories are delimited by `/`.
- `dest` is the absolute or relative destination in the container; a relative path is resolved against the container's `WORKDIR`.
- By default matched files keep their whole directory hierarchy below the context; `strip` removes a path prefix. With `strip: content/en/`, `content/en/sub/index.md` lands at `content/sub/index.md`.
- A pattern like `static-html/*.html` does not match files in sub-folders.

Infer mode:

```yaml
  sync:
    infer: ["**/*.js"]
```

`infer` is a list of glob patterns for files eligible to sync. Skaffold infers destinations from the `ADD` and `COPY` instructions of the Dockerfile (Docker and Kaniko artifacts, and custom artifacts that explicitly declare a dependency on a Dockerfile). For multi-stage Dockerfiles only the last stage is examined; use manual rules for copies from other stages. For Docker artifacts, only modified and added files sync: deleting a file causes a full rebuild. The ko builder can sync static content with infer, and its rules apply to added, modified and deleted files.

Mixing `manual`, `infer` and `auto` is currently not allowed. Limits: the container user must be able to modify the files, the container needs `tar`, and only local source files sync.

A rule that is too broad can copy files into a path your application never reloads. Test one change in `skaffold dev` and confirm the application picked it up before relying on it.

## Checked

2026-11-04. Read the Skaffold File Sync page and the `Sync` and `SyncRule` definitions in the v4beta14 schema. Confirmed rule fields and semantics, the `strip` example, infer behaviour, the last-stage and deletion rules, ko behaviour and limitations. Removed: the claims that unmatched changes always fall back to build and deploy in a fixed precedence, that "sync is for development; not in CI", and that ko "can delete files" without the infer context. Replaced the earlier example paths with ones taken from the page's own rules.
Method: documentation only; no commands were run.
