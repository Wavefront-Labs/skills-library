---
id: computing-software.cloud-infrastructure-engineering.terraform.releasing-providers-with-goreleaser-and-gpg
name: releasing-providers-with-goreleaser-and-gpg
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, goreleaser, provider-release, gpg-signing, terraform-registry, github-actions, provider-development, registry-manifest]
level: advanced
status: docs-checked
description: "Release a Terraform provider with GoReleaser and a GPG-signed SHA256SUMS from GitHub Actions, including the registry manifest, key requirements and failed-release recovery."
sources: ["https://developer.hashicorp.com/terraform/registry/providers/publishing", "https://github.com/hashicorp/terraform-provider-scaffolding-framework/blob/main/.goreleaser.yml", "https://goreleaser.com/customization/sign/", "https://github.com/crazy-max/ghaction-import-gpg"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Releasing a provider with GoReleaser and GPG

The registry needs, per version: one zip per os/arch, a `SHA256SUMS` file, a detached
GPG signature of it, and a manifest declaring the plugin protocol. GoReleaser produces
all of it from a tag.

## 1. Signing key
- RSA or DSA. The Registry API accepts both RSA and DSA keys, but not the default ECC
  type, so choose RSA when you generate the key (HashiCorp points to GitHub's GPG key
  instructions; the key does not need to be added to GitHub).
- Register the ASCII-armored public key (`gpg --armor --export "{Key ID or email address}"`)
  under **User Settings > Signing Keys** in the Registry before the first release; keys can
  be added for your personal namespace or any organization where you are an admin.
- Store the private key and passphrase as
  CI secrets `GPG_PRIVATE_KEY` and `PASSPHRASE`. Keep an offline backup.

## 2. Repo files
`terraform-registry-manifest.json` (protocol 6.0 for the Plugin Framework, 5.0 for SDKv2):
```json
{ "version": 1, "metadata": { "protocol_versions": ["6.0"] } }
```
`.goreleaser.yml` (abridged from the HashiCorp scaffolding repo, which also builds
`s390x`, has a `go mod tidy` hook and more `ignore` entries; copy it from there):
```yaml
version: 2
builds:
  - env: [CGO_ENABLED=0]
    mod_timestamp: '{{ .CommitTimestamp }}'
    flags: [-trimpath]
    ldflags: ['-s -w -X main.version={{.Version}} -X main.commit={{.Commit}}']
    goos: [freebsd, windows, linux, darwin]
    goarch: [amd64, '386', arm, arm64]
    ignore: [{ goos: darwin, goarch: '386' }]
    binary: '{{ .ProjectName }}_v{{ .Version }}'
archives:
  - formats: [zip]
    name_template: '{{ .ProjectName }}_{{ .Version }}_{{ .Os }}_{{ .Arch }}'
checksum:
  extra_files: [{ glob: terraform-registry-manifest.json, name_template: '{{ .ProjectName }}_{{ .Version }}_manifest.json' }]
  name_template: '{{ .ProjectName }}_{{ .Version }}_SHA256SUMS'
  algorithm: sha256
signs:
  - artifacts: checksum
    args: ["--batch", "--local-user", "{{ .Env.GPG_FINGERPRINT }}", "--output", "${signature}", "--detach-sign", "${artifact}"]
release:
  extra_files: [{ glob: terraform-registry-manifest.json, name_template: '{{ .ProjectName }}_{{ .Version }}_manifest.json' }]
changelog:
  disable: true
```

## 3. Workflow
```yaml
on: { push: { tags: ['v*'] } }
permissions: { contents: write }
jobs:
  goreleaser:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-go@v5
        with: { go-version-file: go.mod }
      - id: import_gpg
        uses: crazy-max/ghaction-import-gpg@v6
        with:
          gpg_private_key: ${{ secrets.GPG_PRIVATE_KEY }}
          passphrase: ${{ secrets.PASSPHRASE }}
      - uses: goreleaser/goreleaser-action@v6
        with: { args: release --clean }
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GPG_FINGERPRINT: ${{ steps.import_gpg.outputs.fingerprint }}
```
The action versions above are illustrative: pin the versions used in the scaffolding
repo's `.github/workflows/release.yml`.

Release by pushing `vX.Y.Z`. The public registry (repo named `terraform-provider-{NAME}`,
public on GitHub, lowercase name, published once via **Publish > Provider** in the
Registry UI) creates a webhook on the repo and ingests new GitHub releases from it.

## 4. Dry runs and recovery
- Run GoReleaser locally without publishing (see the GoReleaser docs for snapshot and
  skip options) to check archive names and platforms before tagging.
- The Registry validates that each release is signed with a key registered for the
  namespace, so a missing or bad signature will not publish. If the webhook is missing
  or not working, remove existing `registry.terraform.io` webhooks on the repo, then
  use the **Resync** button on the provider settings page.

## Gotchas
- Binary name must be `terraform-provider-{NAME}_v{VERSION}`; the `_v` prefix matters.
- The tag must be a valid Semantic Version preceded by `v` (for example `v1.2.3`), and no
  branch may have the same name as the tag.
- HashiCorp notes GoReleaser does not support signing with a GPG key that requires a
  passphrase unless the passphrase is cached; the scaffolding workflow passes `passphrase`
  to the import action. If that fails, sign the checksums manually before publishing.
- `fetch-depth: 0` is required or GoReleaser cannot find the previous tag.

## Verify
- [ ] The GitHub release has every zip, `_SHA256SUMS`, `_SHA256SUMS.sig` and `_manifest.json`.
- [ ] `_SHA256SUMS.sig` is a binary (not ASCII-armored) GPG signature of `_SHA256SUMS`, made with the registered key.
- [ ] `terraform init` with the new version constraint installs on linux and darwin.

## Checked
- 2026-10-28. Confirmed against the Terraform Registry "Publish providers" page: repo name pattern `terraform-provider-{NAME}` and public, `v`-prefixed SemVer tag, manifest `protocol_versions` (5.0 for SDKv2, 6.0 for the Framework), RSA and DSA accepted but not the default ECC type, binary and archive naming, `_SHA256SUMS`, `_SHA256SUMS.sig` binary signature and `_manifest.json`, webhook and Resync; the scaffolding-framework `.goreleaser.yml` and `release.yml` (signs args, checksum, release extra_files, `fetch-depth: 0`, `crazy-max/ghaction-import-gpg` outputs, `release --clean`).
- Removed: the 4096-bit key size, ed25519 wording, key-rotation and immutability claims, the private-registry upload script, GoReleaser v1 `format: zip` note, `--skip=sign` flag and `gpg --verify` command (not in fetched docs).
Method: documentation only; no commands were run.
