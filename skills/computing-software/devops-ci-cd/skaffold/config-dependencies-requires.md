---
id: computing-software.devops-ci-cd.skaffold.config-dependencies-requires
name: config-dependencies-requires
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [requires, dependencies, git, google-cloud-storage, remote]
level: advanced
status: docs-checked
description: "Import other skaffold configs by path, git repository or GCS bucket with requires, and control how remote configs are cached."
sources:
  - "https://skaffold.dev/docs/design/config/"
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`requires` imports configs from other places. Local form:

```yaml
requires:
- path: ../shared/skaffold.yaml
  configs: [base]
```

If `configs` is omitted, all configs in the file at `path` are imported. If `path` is omitted, the required configs are assumed to be in the same file as the current config.

Remote forms:

```yaml
requires:
- git:
    repo: https://git.example.com/team/shared-config.git
    path: skaffold.yaml
    ref: main
  configs: [base]
- googleCloudStorage:
    source: gs://my-bucket/configs/*
    path: skaffold.yaml
```

Behaviour and flags documented:

- Remote contents are downloaded to a cache directory. Set it with `--remote-cache-dir` or `SKAFFOLD_REMOTE_CACHE_DIR`; the default is `~/.skaffold/remote-cache`. Git subdirectories are named by a hash of the repo URI and branch/ref, GCS ones by a hash of the `source`. A remote config is then treated like a local one.
- `--sync-remote-cache` accepts `always` (default), `missing` or `never`: `always` syncs remote repositories to latest on access, `missing` clones only if absent locally, `never` leaves updating to you.
- Profiles passed with `--profile` propagate into imported configs that define them. `--propagate-profiles=false` stops that. For finer control use `activeProfiles` on a `requires` entry: `name` is a profile that must exist in the required configs, `activatedBy` lists profiles of the current config that trigger it; without `activatedBy` it always applies.
- Skaffold ensures artifacts of a required config are built before those of the current config (provided the artifacts have dependencies defined), and required deploys are applied before the current config's deploys.
- `--module cfg1` filters to that module but also includes the transitive closure of its dependencies.
- Files in an imported config are resolved relative to that config's file location.

Pin `ref` to a tag or commit for reproducible builds. `--sync-remote-cache=missing` avoids re-syncing repositories that already exist in the cache.

A common arrangement is a shared repository holding platform configs such as ingress or databases, imported by each service repository. Run `skaffold diagnose --yaml-only` to inspect the effective configuration.

## Checked

2026-11-04. Read the Skaffold "Skaffold Pipeline" (design/config) page, sections Multiple configuration support and Configuration dependencies, and the CLI reference for the cache flags. Confirmed the local and remote `requires` forms, defaults, cache location and hashing, profile propagation and `activeProfiles`, ordering, `--module` closure and path resolution. Removed: the "use in CI" framing beyond what the flag description says, and the unconditional claim that required builds always precede current builds (the page qualifies it). Changed the placeholder repo URL. Note: `skaffold diagnose` documents `--sync-remote-cache` default `missing` while its own text says `always` is the default.
Method: documentation only; no commands were run.
