---
id: computing-software.software-engineering.rust.binary-releases-with-cargo-dist
name: binary-releases-with-cargo-dist
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-release-ci, rust-cargo-dist, cargo-dist, dist, releases, installers, github-releases]
level: practitioner
status: docs-checked
description: "Automate multi-platform Rust binary releases with dist (cargo-dist): init, generated GitHub CI, installers, checksums and the plan/build workflow."
sources:
  - https://github.com/axodotdev/cargo-dist
  - https://axodotdev.github.io/cargo-dist/book/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Binary releases with dist (cargo-dist)

**Goal:** push a tag, get archives and install scripts for each OS/arch.

`dist` (formerly cargo-dist) is a souped-up `cargo build` that builds tarballs and installers and can generate GitHub CI to orchestrate itself and upload to a GitHub Release.

```bash
dist init            # interactive; rerun any time to change settings or update dist (use --yes to accept defaults)
dist plan            # what a release would build; runs the same logic as the generated CI, without building
dist build           # build for the current platform
git tag v0.1.0 && git push --tags    # a properly formatted version tag triggers the generated CI
```

`dist init` writes dist config (in `dist-workspace.toml` or `dist.toml`, or for existing Rust users in `[workspace.metadata.dist]` in `Cargo.toml`: the config is mid-migration, so check your version), adds a shippable build profile and generates `.github/workflows/release.yml`. It often errors on missing `repository` URLs in `Cargo.toml`; fix and rerun, no work is lost.

Key config keys: `cargo-dist-version`, `targets`, `installers`, `ci`, `pr-run-mode`, and `checksum` (default `"sha256"`, which generates a `.sha256` file per archive; `"false"` disables checksums). A plan step runs on every pull request by default; `pr-run-mode = "upload"` also builds and uploads artifacts but is slow and wasteful, so keep it temporary.

Outputs: archives (zip or tarball; defaults to `.zip` on Windows and `.tar.xz` elsewhere) containing the binaries plus auto-detected README, LICENSE and CHANGELOG files; installers: `shell` (`curl | sh`), `powershell` (`irm | iex`), `npm`, `homebrew` and `msi`. Fetching installers (shell, powershell, npm, homebrew) download archives from where you hosted them; the bundling `msi` contains the binaries and is single-platform. The generated release.yml plans from the tag, builds on machines for each platform, publishes to package managers, creates or edits the GitHub Release and adds release notes from your CHANGELOG/RELEASES file.

dist does not prepare the release itself: update the crate version, commit, push, then push the tag.

## Gotchas
- Rerun `dist init` after upgrading dist; hand edits to generated workflow YAML may be overwritten.
- Code signing is not automatic: macOS and Windows each need their own platform-specific approach, so plan for it separately.
- Installer scripts fetch from GitHub, so they are not locally runnable from a `dist build`.
- Builds use `--profile=dist` and, for windows-msvc, append `-Ctarget-feature=+crt-static` to `RUSTFLAGS`.

## Verify
`dist plan` output matches what you expect for the tag; open a PR to see the plan step run; after a release, run the installer and `app --version`.

## Checked
Read the cargo-dist README on GitHub and the dist book pages Rust Quickstart, Installers, Archives and the config reference (installed from the axodotdev.github.io book location, since opensource.axo.dev did not resolve). Removed: the `cargo install cargo-dist --locked` command, the specific tag and version numbers, the target triple list, the `--artifacts=local` flag, the release-plz/cargo-release/cross comparisons, the notarisation and musl notes, and the pipe-to-shell hardening advice (none appeared on pages read).

Method: docs-checked 2026-11-09 against the cargo-dist GitHub README and the dist book quickstart, installers, archives and config reference pages.
