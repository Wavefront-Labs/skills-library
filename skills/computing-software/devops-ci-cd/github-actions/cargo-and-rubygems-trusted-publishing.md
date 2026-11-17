---
id: computing-software.devops-ci-cd.github-actions.cargo-and-rubygems-trusted-publishing
name: cargo-and-rubygems-trusted-publishing
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, cargo-publish, rubygems-trusted-publishing, crates-io-trusted-publishing, release-gem]
level: practitioner
status: docs-checked
description: "Publish Rust crates and Ruby gems from Actions with OIDC trusted publishing (crates-io-auth-action, rubygems/release-gem) instead of stored API tokens."
sources: ["https://github.com/rust-lang/crates-io-auth-action", "https://guides.rubygems.org/trusted-publishing/", "https://github.com/rubygems/release-gem"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cargo and RubyGems trusted publishing

Both registries exchange the job's GitHub OIDC token for a short-lived publish token. Configure the
trusted publisher once on the registry (RubyGems takes owner, repository, workflow name and an optional
environment; see crates.io's own trusted publishing page for its fields).

## 1. crates.io
```yaml
on: { push: { tags: ['v*'] } }
permissions: { contents: read, id-token: write }
jobs:
  publish:
    runs-on: ubuntu-latest
    environment: release
    steps:
      - uses: actions/checkout@v4
      - uses: rust-lang/crates-io-auth-action@v1
        id: auth
      - run: cargo publish
        env: { CARGO_REGISTRY_TOKEN: "${{ steps.auth.outputs.token }}" }
```
Workspaces: publish crates in dependency order (`cargo publish -p core` then `-p cli`), or use
`cargo publish --workspace`. The action's post step revokes the token when the job completes; the
`url` input selects a different registry (for example the crates.io staging site).
Pre-flight: `cargo publish --dry-run` in PR CI.

## 2. RubyGems
rubygems.org → gem page → **Trusted publishers** → Create (a *pending* trusted publisher allows the first release of a new gem).
```yaml
permissions: { contents: write, id-token: write }
steps:
  - uses: actions/checkout@v4
  - uses: ruby/setup-ruby@v1
    with: { bundler-cache: true, ruby-version: ruby }
  - uses: rubygems/release-gem@v1     # trusted publishing; runs the bundler release tasks
```
`rake release` (bundler release tasks) pushes the release tag — hence `contents: write`. Put
`id-token: write` at job level (recommended). The action expects checkout, a Ruby environment, bundler
and the bundler release tasks. If you set a GitHub environment on RubyGems, the job must use it.

## 3. Gotchas
- Workflow filename and environment must match the registry config exactly.
- Version must be bumped in `Cargo.toml` / `version.rb` before tagging.
- Remove old `CARGO_REGISTRY_TOKEN` / `RUBYGEMS_API_KEY` secrets once migrated.

## Verify
- [ ] A release publishes with no registry secret configured.

## Checked

2026-10-31. Confirmed against the RubyGems Trusted Publishing guide, the rubygems/release-gem README (id-token: write and contents: write, bundler release tasks requirement), the rust-lang/crates-io-auth-action README (token output, automatic revocation in the post step, url input) and the Cargo cargo-publish manual (--workspace, --package, --dry-run).
Removed: the crates.io first-release-manual rule, the crates.io settings path, the 30 minute token lifetime, the Cargo 1.90 version gate, cargo package --list, the configure-rubygems-credentials fallback and the crates.io documentation source (the page is not readable by script).

Method: documentation only; no commands were run.
