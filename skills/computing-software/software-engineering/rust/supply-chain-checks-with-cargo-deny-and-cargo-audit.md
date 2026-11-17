---
id: computing-software.software-engineering.rust.supply-chain-checks-with-cargo-deny-and-cargo-audit
name: supply-chain-checks-with-cargo-deny-and-cargo-audit
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo, cargo-deny, cargo-audit, supply-chain, rustsec, licenses, cargo-vet, rust-security]
level: practitioner
status: docs-checked
description: "Guard Rust dependencies with cargo-audit and cargo-deny: RustSec advisories, license allowlists, banned and duplicate crates, source restrictions, and CI enforcement."
sources:
  - https://github.com/rustsec/rustsec/tree/main/cargo-audit
  - https://embarkstudios.github.io/cargo-deny/
  - https://rustsec.org/
  - https://mozilla.github.io/cargo-vet/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Supply chain checks with cargo-deny and cargo-audit

**Goal:** vulnerable, unmaintained, wrongly licensed or unexpected-source crates are blocked before merge.

## 1. cargo-audit (vulnerabilities)
```bash
cargo install cargo-audit --locked      # add --features=fix for `cargo audit fix`
cargo audit                          # checks Cargo.lock against the RustSec advisory DB
cargo audit --deny warnings          # also fail on unmaintained/yanked warnings
cargo audit fix --dry-run            # suggest upgrades
cargo audit bin target/release/app   # audit a binary built with cargo-auditable
```
Ignore advisories in `.cargo/audit.toml` (project) or `~/.cargo/audit.toml`, or pass `--ignore`:
```toml
[advisories]
ignore = ["RUSTSEC-2023-0071"]       # rsa timing sidechannel; we do not use RSA decryption
```

## 2. cargo-deny (policy)
```bash
cargo install cargo-deny --locked
cargo deny init
cargo deny check                     # advisories, bans, licenses, sources
```
```toml
# deny.toml
[advisories]
yanked = "deny"
ignore = [{ id = "RUSTSEC-2024-0384", reason = "instant unmaintained; transitive via notify, no fix yet" }]

[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Unicode-3.0", "Zlib"]
confidence-threshold = 0.9
[[licenses.clarify]]
crate = "webpki"
expression = "ISC"
license-files = [{ path = "LICENSE", hash = 0x001c7e6c }]

[bans]
multiple-versions = "warn"           # duplicate major versions bloat builds
wildcards = "deny"
deny = [{ crate = "openssl", reason = "use rustls" }]
skip-tree = []

[sources]
unknown-registry = "deny"
unknown-git = "deny"
allow-git = ["https://github.com/acme/internal-fork"]
```

## 3. CI
```yaml
- uses: EmbarkStudios/cargo-deny-action@v2
  with: { command: check }
```
Run advisories on a schedule too (daily), since new advisories appear for unchanged lockfiles.

## 4. Going further
- `cargo-vet`: require an audit for each crate version.
- `cargo auditable` embeds the dependency list into binaries so `cargo audit bin` can scan deployed artifacts accurately.
- `cargo tree -d` shows duplicate versions; `cargo tree -i <crate>` who pulls it in.

## Gotchas
- Advisories for crates you do not call can still matter (transitive use); read the advisory's affected functions before ignoring.
- License detection uses a confidence score (default threshold 0.8); use `clarify` for crates whose license cannot be read automatically.
- `multiple-versions = "deny"` is often unrealistic; warn and track.

## Verify
- `cargo deny check` passes locally and in CI; adding a GPL crate or a git dependency from an unknown host fails the check.

## Checked

2026-10-25. Checked against the cargo-audit README and source (`cargo audit fix` needs the `fix` feature, `--dry-run`, `cargo audit bin`, `--deny warnings`, `audit.toml` locations, `[advisories] ignore`), the cargo-deny documentation (advisories `yanked` and `ignore` with `reason`; licenses `allow`, `confidence-threshold` default 0.8, `clarify` with `license-files` and hash; bans `multiple-versions`, `wildcards`, `deny` with `reason`, `skip-tree`; sources `unknown-registry`, `unknown-git`, `allow-git`), the cargo-deny-action README (`@v2`, `command`, default `check`) and the RustSec advisory database entries RUSTSEC-2023-0071 (rsa, Marvin attack) and RUSTSEC-2024-0384 (instant, unmaintained). Wrong in the draft and fixed: cargo-audit has no expiry setting in `audit.toml`; `cargo audit fix` needs an optional feature; the action example passed check names in `command`. Removed unconfirmed vendor and tool remarks.

Method: documentation only; no commands were run.
