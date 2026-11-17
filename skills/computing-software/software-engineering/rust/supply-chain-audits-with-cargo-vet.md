---
id: computing-software.software-engineering.rust.supply-chain-audits-with-cargo-vet
name: supply-chain-audits-with-cargo-vet
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-security, rust-cargo-vet, cargo-vet, cargo-crev, supply-chain, audits, trust]
level: advanced
status: docs-checked
description: "Adopt cargo-vet to record audits for third-party crates, import trusted audit sets, handle exemptions and enforce it in CI."
sources:
  - https://mozilla.github.io/cargo-vet/
  - https://github.com/mozilla/cargo-vet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Supply-chain audits with cargo-vet

**Goal:** every third-party crate version is either audited by someone you trust or consciously exempted.

Setup, from the top-level project directory:

```bash
cargo vet            # before setup: "cargo vet is not configured"
cargo vet init       # creates supply-chain/ next to Cargo.lock with audits.toml and config.toml
cargo vet            # "Vetting Succeeded (X exempted)"
```

`init` fills the `exemptions` table of `config.toml` with every current third-party crate, so vetting passes with an empty audit set. Commit the `supply-chain` files with `Cargo.lock`. Avoid adding exemptions and shrink the list over time. The directory location is configurable.

Record audits in `audits.toml`. Each entry has exactly one of `version` (audited in full), `delta` (the diff between two versions was audited) or `violation` (the crate does not meet the criteria; takes a version requirement such as `*` or `>=2.0, <2.3`), plus `who` and `criteria`:

```toml
[[audits.bar]]
version = "1.2.3"
who = "Alice Foo <alicefoo@example.com>"
criteria = "safe-to-deploy"

[[audits.bar]]
delta = "1.2.3 -> 1.2.4"
who = "Bob Bar <bobbar@example.com>"
criteria = "safe-to-deploy"
```

Do not prune `audits.toml` unless an entry was erroneous; records stay useful to others.

Import audit sets from organisations you trust with `imports` in `config.toml`:

```toml
[imports.foo]
url = "https://raw.githubusercontent.com/foo-team/foo/main/supply-chain/audits.toml"
```

`cargo vet` fetches each URL and stores the data in `imports.lock`; `--locked` skips the fetch. Imports are not transitive. The cargo-vet repository keeps a registry (`registry.toml`) of well-known audit sets, and suggestions surface importable entries from it.

Criteria: built-in `safe-to-run` and `safe-to-deploy` (which implies `safe-to-run`) mean the same in every project. Define custom criteria in `audits.toml` with `[criteria.name]` and a `description`; foreign custom criteria have no meaning locally unless mapped. Use policy to relax or tighten per crate, for example `[policy.mycrate]` with `criteria = ["safe-to-deploy"]` and `dependency-criteria = { non-exposed-crate = ["safe-to-run"] }`. With aggregated audits, each criteria `description` must be exactly identical in every repository.

CI: run `cargo vet --locked` on push and pull request so every change has a fully vetted dependency set. The cargo-vet book's GitHub Actions example caches the installed binary (`cargo install --root ... --version $CARGO_VET_VERSION cargo-vet`) so results appear in seconds rather than minutes.

## Gotchas
- An imported audit is only as good as its issuer; custom criteria from a foreign file need explicit mapping.
- Dependencies' own `audits.toml` files have no effect unless you import them.

## Verify
Add a new dependency in a branch and confirm CI fails until an audit or exemption is added.

## Checked
2026-11-08. Read in full from the cargo-vet book source (book/src in the cargo-vet repository, same content as the published book): Setup, Audit Criteria, Importing Audits, Recording Audits, Configuring CI, Built-In Criteria. Confirmed: init behaviour and files, exemptions, audit entry fields and sample, imports.lock and --locked, registry, built-in and custom criteria, policy example, CI job. Removed (not on the pages read): the inspect, certify, diff and suggest command lines, install command, the mozilla and google import URLs, cargo-crev, cargo deny and cargo audit comparisons, and build-script advice.
Method: documentation only; no commands were run.
