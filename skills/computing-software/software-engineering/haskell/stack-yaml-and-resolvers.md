---
id: computing-software.software-engineering.haskell.stack-yaml-and-resolvers
name: stack-yaml-and-resolvers
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, stack, stack-yaml, resolver, lts, nightly, extra-deps, package-yaml, hpack, stackage-snapshot, stack-yaml-and-resolvers, haskell-stack]
level: practitioner
status: docs-checked
description: "Configure Stack with stack.yaml: snapshot (LTS or Nightly, resolver deprecated), packages, extra-deps from Hackage, git or GitHub, flags, ghc-options and the Stack root."
sources: ["https://docs.haskellstack.org/en/stable/configure/yaml/project/", "https://docs.haskellstack.org/en/stable/configure/yaml/non-project/", "https://docs.haskellstack.org/en/stable/topics/stack_root/", "https://docs.haskellstack.org/en/stable/commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# stack.yaml and snapshots

**Goal:** reproducible builds using a curated Stackage snapshot.

```yaml
# stack.yaml
snapshot: lts-24.43            # Stackage LTS; 'resolver' is a deprecated synonym
packages:
  - .
extra-deps:
  - acme-missiles-0.3          # a package from Hackage (version required)
  - git: https://github.com/example-user/my-repo.git
    commit: '<sha>'            # quote it: an all-digit hash would be a YAML number
  - github: example-user/my-repo
    commit: '<sha>'
flags:
  mypkg:
    fast: true
ghc-options:
  "$locals": -Wall
```

## Facts
- A snapshot fixes a GHC version and a set of package versions: a Stackage LTS Haskell snapshot (`lts-24.43`) or a Nightly one (`nightly-2026-05-29`).
- `stack new PACKAGE_NAME` creates a project from a template; `stack setup` installs GHC and, on Windows, MSYS2.
- Project-level config is `stack.yaml`; global config is `config.yaml` in the Stack root, whose location depends on the OS and on `STACK_XDG`.
- `stack ls dependencies`, `stack clean`, `stack path`, `stack haddock` exist; see the commands page.
- Each project package directory must have a Cabal file or an Hpack `package.yaml`.
- An extra-dep shadows a snapshot package of the same name, and a GHC boot package with the same name and version is ignored.

## Gotchas
- A package that is not in the snapshot goes in `extra-deps`; a Hackage entry must include the version, and its own missing dependencies need entries too.
- A local path that looks like a package identifier is read as a Hackage package; prefix it with `./`.
- `work-dir` (non-project config) sets where build output goes; `stack clean` removes build artefacts.

## Self-check
- [ ] `stack build --test` passes from a clean clone.
- [ ] `extra-deps` entries are pinned to exact versions or commits.

## Checked
2026-11-03. Confirmed against the Stack docs (project config, non-project config, stack root, new, setup, ls, clean commands): `snapshot`/`resolver`, LTS and Nightly names, `extra-deps` forms (Hackage, git, github with quoted commit), `flags`, `$locals` in `ghc-options`, `work-dir`, hpack `package.yaml`, MSYS2 on Windows, shadowing rules. Removed: the `nix:` stanza, the hpack example, the "not in snapshot" message, `.gitignore` advice, `stack exec`/`stack run` list, `~/.stack` path.
Method: documentation only; no commands were run.
