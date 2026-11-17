---
id: computing-software.devops-ci-cd.github-actions.goreleaser-in-github-actions
name: goreleaser-in-github-actions
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, goreleaser, goreleaser-action, go-release-automation, goreleaser-snapshot]
level: practitioner
status: gated
description: "Release Go binaries with GoReleaser in Actions: .goreleaser.yaml v2, goreleaser-action, full history checkout, snapshot builds in PRs, checksums, signing and Homebrew taps."
sources: ["https://goreleaser.com/ci/actions/", "https://goreleaser.com/customization/", "https://github.com/goreleaser/goreleaser-action"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GoReleaser in GitHub Actions

## 1. Config
```yaml
# .goreleaser.yaml
version: 2
before:
  hooks: [go mod tidy]
builds:
  - env: [CGO_ENABLED=0]
    goos: [linux, darwin, windows]
    goarch: [amd64, arm64]
    ldflags: ["-s -w -X main.version={{.Version}} -X main.commit={{.Commit}}"]
archives:
  - formats: [tar.gz]
    format_overrides: [{ goos: windows, formats: [zip] }]
checksum:
  name_template: checksums.txt
changelog:
  use: github-native            # or git with filters
```
Validate locally with `goreleaser check` and `goreleaser release --snapshot --clean` (flag semantics were not confirmed in the pages read; gated: unconfirmed, source is paywalled or blocked).

## 2. Workflow
```yaml
on: { push: { tags: ['v*'] } }
permissions: { contents: write }
jobs:
  goreleaser:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with: { fetch-depth: 0 }          # required: GoReleaser needs the full commit history
      - uses: actions/setup-go@v7
        with: { go-version-file: go.mod }
      - uses: goreleaser/goreleaser-action@v7
        with: { distribution: goreleaser, version: '~> v2', args: release --clean }
        env: { GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}" }
```
In PR CI run the same action with `args: release --snapshot --clean` to catch config breakage before tagging.

## 3. Extras
- Homebrew tap / Scoop bucket live in other repos; the Homebrew casks docs show an optional per-publisher `token` for when it differs from the default token. Whether `GITHUB_TOKEN` can push there, and the section name for formulae (`brews`), were not confirmed (gated: unconfirmed, source is paywalled or blocked).
- Signing: a `signs:` block with `artifacts: checksum`; the GoReleaser CI docs show cosign with `--bundle=${signature}` (one `.sigstore.json` file combining certificate and signature) and note `id-token: write` is needed for cosign with GitHub OIDC. Check the exact args in the signing docs (the `--output-signature` flag was not confirmed; gated: unconfirmed, source is paywalled or blocked).
- Docker images: see the GoReleaser docker and docker_manifest docs (`dockers_v2` was not confirmed; gated: unconfirmed, source is paywalled or blocked).
- A dirty git tree fails the release (not confirmed in the pages read; gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Snapshot job green on PRs.
- [ ] Tagged release has archives for every os/arch plus `checksums.txt`.

## Checked

2026-11-02. Confirmed against the GoReleaser CI/Actions docs and the goreleaser-action README: fetch-depth: 0 is required (full commit history), distribution: goreleaser and version: '~> v2', current examples use actions/checkout, actions/setup-go and goreleaser-action at v7, cosign signing with a --bundle .sigstore.json file and id-token: write; homebrew_casks docs. Fixed: action version pins (v4/v5/v6 to v7). Removed: brews[].repository.token, dockers_v2 requirement text, dirty-tree wording. Gated: --snapshot semantics, --output-signature flag, brews section, dockers_v2, dirty-tree failure.

Method: documentation only; no commands were run.
