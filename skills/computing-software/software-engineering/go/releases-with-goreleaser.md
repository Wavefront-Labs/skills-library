---
id: computing-software.software-engineering.go.releases-with-goreleaser
name: releases-with-goreleaser
category: computing-software
field: software-engineering
product: go
tags: [go, go-release-ops, go-goreleaser, goreleaser, release, changelog, checksums]
level: practitioner
status: docs-checked
description: "Automate Go releases with GoReleaser: multi-platform archives, checksums, changelog and a dry-run snapshot."
sources:
  - https://goreleaser.com/customization/
  - https://goreleaser.com/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Releases with GoReleaser

**Goal:** tag a commit and get archived, checksummed binaries for every platform.

Start from `goreleaser init`, which writes an example `.goreleaser.yaml` to check into source control. An example of the sections used here (the documented default `ldflags` already inject `main.version` and `main.commit`):

```yaml
before:
  hooks:
    - go mod tidy
builds:
  - main: ./cmd/app
    env: [CGO_ENABLED=0]
    goos: [linux, darwin, windows]
    goarch: [amd64, arm64]
archives:
  - formats: [tar.gz]
    format_overrides:
      - goos: windows
        formats: [zip]
checksum:
  name_template: "{{ .ProjectName }}_checksums.txt"
changelog:
  sort: asc
  filters:
    exclude: ["^docs:"]
```

```bash
goreleaser check                       # validate config
goreleaser release --snapshot --clean  # local dry run from the latest commit, no publish
goreleaser healthcheck                 # are the tools the config needs available
git tag -a v0.1.0 -m "First release" && git push origin v0.1.0
goreleaser release --clean             # releases from the latest git tag; needs GITHUB_TOKEN
```

`--clean` removes files from earlier runs in `dist` (the default distribution directory). The default `ldflags` are `-s -w -X main.version={{.Version}} -X main.commit={{.Commit}} -X main.date={{.Date}} -X main.builtBy=goreleaser`. Archives default to `tar.gz`; `zip`, `tar.xz`, `tar.zst`, `binary` and others are valid formats. The checksum file defaults to `{{ .ProjectName }}_{{ .Version }}_checksums.txt` using `sha256`. `before.hooks` run before the release starts. SBOMs are configured in an `sboms` section (default command `syft`).

In GitHub Actions use `goreleaser/goreleaser-action` with `fetch-depth: 0` on checkout, which the docs say is required because GoReleaser needs the full commit history; the documented workflow runs only against pushed tags.

## Gotchas
- Releasing to GitHub needs a `GITHUB_TOKEN`: a classic token with the `repo` scope, or a fine-grained token with `contents: write`.
- The singular `format` archive key is marked deprecated in favour of `formats`.
- Check the tag follows semantic versioning.
- Pin the GoReleaser version in CI (the Actions docs use `version: "~> v2"`).

## Verify
`goreleaser release --snapshot --clean` produces `dist/` with archives and a checksums file for each target.

## Checked
2026-11-03. Confirmed on goreleaser.com pages: quick-start (init, check, snapshot, clean, healthcheck, tokens, tag flow), builds (default ldflags, env, goos/goarch), archives (formats, format_overrides, deprecated `format`), checksums (default name, sha256), changelog (sort, filters), hooks, SBOM (syft default), GitHub Actions (fetch-depth: 0, goreleaser-action, `~> v2`). Removed: `version: 2` header and schema-change claim, `go test` hook, `-trimpath` flag, cosign signing, notarisation note, dirty-tree abort claim, `sha256sum` and `--version` verification.
Method: documentation only; no commands were run.
