---
id: computing-software.devops-ci-cd.build-systems.toolchain-pinning-and-hermetic-dev-environments
name: toolchain-pinning-and-hermetic-dev-environments
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, toolchain-pinning, hermetic-dev-environment, hermetic-builds, nix, nix-flakes, devenv, devbox, devcontainers, dev-containers, mise, asdf, tool-versions, rust-toolchain-toml, go-toolchain-directive, node-version, volta, corepack, python-version, uv, pinned-compilers, same-toolchain-ci-and-laptop, works-on-my-machine, flake-lock, nixpkgs-pin, direnv, reproducible-environments, bazel-toolchains, hermetic-cc-toolchain, dockerized-builds]
level: practitioner
status: draft
description: "Make the toolchain part of the repo: pin compilers, runtimes and CLIs with mise/asdf, language-native pin files, devcontainers or Nix flakes, and reuse the same definition in CI."
sources: ["https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake", "https://mise.jdx.dev/", "https://containers.dev/implementors/json_reference/", "https://rust-lang.github.io/rustup/overrides.html", "https://go.dev/doc/toolchain", "https://devenv.sh/", "https://bazel.build/extending/toolchains"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Toolchain pinning and hermetic dev environments

**Goal:** `git clone && <one command>` gives every developer and every CI job the exact
same compiler, runtime and CLI versions — so "works on my machine" and "CI uses a
different Node" stop being categories of bug, and builds become reproducible inputs for
SLSA-style provenance.

## 1. Ladder of hermeticity (pick the lowest rung that solves your pain)
| rung | mechanism | pins | leaks |
|---|---|---|---|
| 1 | language-native version files | one runtime each | system libs, CLIs |
| 2 | **mise**/asdf `.tool-versions`/`mise.toml` | many runtimes + CLIs (node, go, python, terraform, kubectl, jq…) | system libs (openssl, glibc) |
| 3 | **devcontainer** / dockerised builds | whole OS userland | kernel, CPU arch, host Docker |
| 4 | **Nix flakes** / devenv / devbox | everything down to libc, bit-reproducible | kernel; learning curve |
| 5 | Bazel hermetic toolchains | compilers fetched by the build itself | needs Bazel |
Most teams: rung 2 for day-to-day plus rung 3 for CI parity, or rung 4 when a
polyglot/C-heavy repo keeps breaking on system libraries.

## 2. Language-native pins (always do these; they're free)
- **Rust**: `rust-toolchain.toml` (`[toolchain] channel = "1.82.0" components = ["clippy","rustfmt"] targets = [...]`) — rustup auto-installs. `Cargo.lock` committed, even for libraries.
- **Go**: `go 1.23.2` + `toolchain go1.23.2` in `go.mod`; `GOTOOLCHAIN=local` in CI to *forbid* auto-download drift (or `auto` to allow the pinned one only). `go.sum` enforced by default.
- **Node**: `.nvmrc`/`.node-version` (`20.18.0`), `"engines"` + `engine-strict=true` in `.npmrc`; **corepack** pins the package manager (`"packageManager": "pnpm@9.12.0+sha512.…"` in `package.json`; `corepack enable`); lockfile committed, `npm ci`/`pnpm install --frozen-lockfile` in CI.
- **Python**: `.python-version` (`3.12.7`), `uv` (`uv.lock`, `uv python install` honours the pin, `requires-python`), or `poetry.lock`; never bare `pip install` from `requirements.txt` without hashes in CI.
- **Java**: `.sdkmanrc`/`.java-version` + Gradle **toolchains** (`java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }` with foojay resolver) or Maven `maven-toolchains-plugin`; Gradle wrapper `gradle-wrapper.properties` with `distributionSha256Sum`; Maven wrapper (`mvnw`).
- **Ruby**: `.ruby-version` + `Gemfile.lock` + `bundler` version in the lockfile (`BUNDLED WITH`).
- **.NET**: `global.json` (`"sdk": {"version": "8.0.403", "rollForward": "disable"}`), `packages.lock.json` with `RestoreLockedMode`.
- **Terraform/OpenTofu**: `required_version = "~> 1.9.0"`, `.terraform.lock.hcl` committed with hashes for all platforms (`terraform providers lock -platform=linux_amd64 -platform=darwin_arm64`).

## 3. mise (asdf-compatible) for the rest
```toml
# mise.toml (or .tool-versions)
[tools]
node = "20.18.0"
python = "3.12.7"
go = "1.23.2"
terraform = "1.9.8"
kubectl = "1.31.1"
"github.com/golangci/golangci-lint" = "1.61.0"   # go: backend / ubi/aqua backends for GitHub release binaries
[env]
_.file = ".env.ci"
```
`mise install` on a laptop and `jdx/mise-action` in GitHub Actions (or `mise install` in
any CI image) → identical versions. `mise trust`, `mise x -- cmd` to run with the pinned
toolchain, `mise run build` as a task runner. Pin exact versions, not `latest`; update
via Renovate (`mise` manager supported) in reviewed PRs. Limits: binaries still link to
the host's libc/openssl — fine until it isn't (Python wheels, C extensions).

## 4. Devcontainers: the CI image is the dev image
`.devcontainer/devcontainer.json` references a **Dockerfile you also use in CI**:
```json
{ "name": "app", "build": { "dockerfile": "../ci/Dockerfile", "target": "dev" },
  "features": { "ghcr.io/devcontainers/features/docker-in-docker:2": {} },
  "postCreateCommand": "mise install && pre-commit install",
  "remoteUser": "vscode" }
```
Publish the image (`ghcr.io/example/ci-base:<digest>`) from a pipeline; CI jobs use
`container: image: ghcr.io/example/ci-base@sha256:…` (GitHub) / `image:` (GitLab) /
`agent { docker { image … } }` (Jenkins); developers open it in VS Code/JetBrains/
Codespaces; `devcontainer build`/`devcontainer up` CLI for scripted use. Pin the base
image by digest and bump with Renovate. Result: one definition, three consumers.

## 5. Nix flakes (full hermeticity)
```nix
# flake.nix
{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  outputs = { self, nixpkgs }:
    let forAll = f: nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" ] (s: f nixpkgs.legacyPackages.${s});
    in {
      devShells = forAll (pkgs: { default = pkgs.mkShell { packages = with pkgs; [ go_1_23 nodejs_20 python312 terraform kubectl golangci-lint ]; }; });
      packages  = forAll (pkgs: { default = pkgs.buildGoModule { pname = "app"; version = "1.4.2"; src = ./.; vendorHash = "sha256-…"; }; });
    };
}
```
`flake.lock` pins nixpkgs by commit → every package version and its transitive libs are
fixed; `nix develop` (or `direnv` with `use flake`) enters the shell; `nix build` makes
the artifact in a sandbox with no network except declared fixed-output fetches —
**hermetic by construction**. CI: `DeterminateSystems/nix-installer-action` + `nix build`,
with a binary cache (Cachix/Attic/S3) so CI doesn't rebuild the world. devenv.sh and
devbox wrap the same engine with friendlier config (`devbox.json` lists packages; no
Nix language needed). Costs: learning curve, disk (`/nix/store`), occasional packages
missing or stale, Docker images produced via `dockerTools` differ from Dockerfiles.

## 6. Bazel toolchains (when you're already there)
Register hermetic toolchains so the build downloads its own compilers: `rules_go`
(`go_register_toolchains(version = "1.23.2")`), `rules_nodejs`/`aspect_rules_js`
(`nodejs_register_toolchains(node_version = "20.18.0")`), `rules_python`
(`python_register_toolchains`), `toolchains_llvm` or `hermetic_cc_toolchain` (zig-based)
for C/C++ — the host compiler is never used; `--incompatible_enable_cc_toolchain_resolution`,
`--sandbox_default_allow_network=false`. Remote cache hits then become portable across
machines, which is the payoff.

## 7. Guardrails in CI
- A job that fails if any pin file changed without a lockfile change (or vice versa).
- `GOTOOLCHAIN=local`, `engine-strict`, `rollForward: disable`, `--frozen-lockfile`:
  make the pipeline refuse to drift silently.
- Print tool versions at the start of every job (`mise ls --current`, `go version`,
  `node -v`) — the first thing you'll want when comparing a laptop with CI.
- Renovate manages: mise/asdf, `.nvmrc`, `rust-toolchain`, `go` directive, Dockerfile
  bases, flake inputs (`nix` manager) — one weekly batch PR per repo.

## Verify
- [ ] Fresh clone on a clean machine: one command (`mise install`/`nix develop`/devcontainer) yields passing tests with zero manual installs.
- [ ] CI logs show the same versions as the laptop for compiler, runtime, package manager.
- [ ] Changing a pinned version in a PR is the only way to change the toolchain (no `latest`, no auto-download drift).
- [ ] Two CI runs of the same commit produce identical artifact hashes (for Nix/Bazel paths) or identical dependency trees (lockfile paths).
