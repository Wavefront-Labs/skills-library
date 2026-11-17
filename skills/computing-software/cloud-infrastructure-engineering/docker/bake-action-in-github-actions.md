---
id: computing-software.cloud-infrastructure-engineering.docker.bake-action-in-github-actions
name: bake-action-in-github-actions
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, bake, bake-action, github-actions, metadata-action, docker-metadata-action, ci-builds]
level: practitioner
status: docs-checked
description: "Drive buildx bake from GitHub Actions with docker/bake-action: metadata-action bake files, cwd:// local files vs Git context, --set overrides for cache and push."
sources: ["https://github.com/docker/bake-action", "https://github.com/docker/metadata-action#bake-definition", "https://docs.docker.com/build/ci/github-actions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docker/bake-action in GitHub Actions

## HCL side: an empty target metadata-action fills in
```hcl
# docker-bake.hcl
target "docker-metadata-action" {}          # tags and labels injected by CI

group "default" { targets = ["app"] }

target "app" {
  inherits  = ["docker-metadata-action"]
  context   = "."
  platforms = ["linux/amd64", "linux/arm64"]
}
```
Locally `docker buildx bake` still works; the inherited target is just empty.

## Workflow
```yaml
jobs:
  bake:
    runs-on: ubuntu-24.04
    permissions: { contents: read, packages: write }
    steps:
      - uses: docker/setup-qemu-action@v4
      - uses: docker/setup-buildx-action@v4
      - uses: docker/login-action@v4
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - id: meta
        uses: docker/metadata-action@v6
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha
      - uses: docker/bake-action@v7
        with:
          files: |
            ./docker-bake.hcl
            cwd://${{ steps.meta.outputs.bake-file }}
          targets: app
          push: ${{ github.event_name != 'pull_request' }}
          set: |
            *.cache-from=type=gha
            *.cache-to=type=gha,mode=max
```

## Context modes (v6 and later)
- Since v6 bake-action builds from the **Git context** of the triggering ref
  (`https://github.com/<owner>/<repo>.git#<ref>`), like `build-push-action`, so no checkout
  is needed.
- Files produced during the job (the metadata bake file) must be referenced with `cwd://`.
- To build from the checked-out workspace instead, add `actions/checkout` and set
  `source: .`. A local `source` path makes Bake run from that directory (as if
  `cd <path> && docker buildx bake`), which affects every relative path: local outputs,
  cache import/export and `cwd://`. `source` also accepts `{{defaultContext}}:subdir`.

## Useful inputs
| Input | Effect |
|---|---|
| `targets` | Targets or groups to build |
| `set` | `--set` overrides, one per line; `*` matches all targets |
| `push` / `load` | Shorthand for `*.output=type=registry` / docker |
| `provenance`, `sbom` | Shorthand for `--set=*.attest=type=provenance` / `type=sbom` |
| `allow` | Grant resources the build may access (for example `network.host`) |
| `vars` | Set Bake variables as key-value pairs or a JSON array |

## Gotchas
- `metadata-action` writes labels and tags for target `docker-metadata-action`; rename via
  its `bake-target` input if your HCL uses another name.
- Keep `push` conditional on the event, as the example does (no push on pull requests).
- metadata-action also has `bake-file-tags`, `bake-file-labels` and `bake-file-annotations`
  outputs; add the one you need to `files` with `cwd://`.

## Checked

Checked 2026-10-23 against the docker/bake-action and docker/metadata-action READMEs (main branch) and the GitHub releases API.

- Current major versions: bake-action v7.5.0, metadata-action v6.2.0, setup-qemu-action v4.4.0, setup-buildx-action v4.4.1, login-action v4.6.0 (the older majors in the first draft were stale).
- Git context default since v6, `source` semantics (local path changes Bake's working directory), `cwd://` for generated files.
- Inputs `targets`, `files`, `set`, `push`, `load`, `provenance`, `sbom`, `allow`, `vars`; metadata-action `bake-target` input and `bake-file*` outputs.
- Removed the fork-push claim's specifics and the `security.insecure` example, which the README does not list.

Method: documentation only; no commands were run.
