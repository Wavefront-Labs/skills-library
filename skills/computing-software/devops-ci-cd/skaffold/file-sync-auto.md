---
id: computing-software.devops-ci-cd.skaffold.file-sync-auto
name: file-sync-auto
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [sync, auto, jib, buildpacks]
level: advanced
status: docs-checked
description: "Let the builder decide what to sync: auto mode for Jib and Buildpacks, and how to turn it off."
sources:
  - "https://skaffold.dev/docs/filesync/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Auto sync delegates discovery of sync rules to the build system. It is available only for Jib and Buildpacks artifacts.

```yaml
artifacts:
- image: app
  jib: {}
  sync:
    auto: true
```

Facts from the docs:

- For Buildpacks, auto sync is on by default. Disable it with `sync: auto: false`.
- The GCP Buildpacks builder (`gcr.io/buildpacks/builder:v1`) syncs Go (`*.go`), Java (`*.java`, `*.kt`, `*.scala`, `*.groovy`, `*.clj`) and NodeJS (`*.js`, `*.mjs`, `*.coffee`, `*.litcoffee`, `*.json`) sources. Buildpacks collaborate by writing sync rules into the image's bill of materials; Skaffold sets `GOOGLE_DEVMODE=1` during `skaffold dev` with auto sync.
- For Jib, auto sync is zero-config: it syncs class files, resource files and Jib "extra directories" files. It works only with Jib in the default (exploded) build mode for non-WAR applications, and was designed around Spring Boot Developer Tools but works with any embedded server that can reload or restart.
- Changes to file types the auto mode does not know trigger a complete rebuild.

Choose among modes:

1. `manual` when you know exactly which files to copy and where (works for every artifact type).
2. `infer` when the destinations can be inferred (Docker and Kaniko Dockerfiles, custom artifacts that declare a Dockerfile dependency, ko static content).
3. `auto` for Jib and Buildpacks, where the builder knows more than you.

You cannot mix `manual`, `infer` and `auto` modes in one artifact's sync configuration; the docs say this is currently not allowed.

General limits of file sync: files must be modifiable by the container's user ID, the container needs the `tar` command, and only local source files can be synced (files created by the builder are not copied).

## Checked

2026-11-04. Read the Skaffold File Sync page (auto mode, Buildpacks, Jib, limitations) and the `Sync` definition in the v4beta14 schema. Confirmed everything above. Removed: the claim that sync events are logged and a rebuild means no rule matched (not on the page), the "start with auto and add manual rules for gaps" advice (the docs say mixing modes is not allowed), and the loose "Jib dev setup" wording.
Method: documentation only; no commands were run.
