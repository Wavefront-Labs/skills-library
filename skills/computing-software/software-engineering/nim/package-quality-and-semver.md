---
id: computing-software.software-engineering.nim.package-quality-and-semver
name: package-quality-and-semver
category: computing-software
field: software-engineering
product: nim
tags: [package-quality-and-semver, nimble-publishing, semver, versioning, package-quality, compatibility, changelog, ci, nim-versions, nim]
level: practitioner
status: docs-checked
description: "Version a Nimble package: requires version operators, tags, deprecation pragma, NimMajor checks, nimble test, and a CI matrix with setup-nim-action or install-nim."
sources:
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/create-packages.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/use-packages.md
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/system.html
  - https://github.com/jiro4989/setup-nim-action
  - https://github.com/iffy/install-nim
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package quality and versioning

Goal: ship releases that dependents can rely on.

- Declare the minimum Nim in the .nimble file: `requires "nim >= 2.0.0"`. Version operators in `requires` include comparisons plus `^=` and `~=`; per the guide `nim ^= 1.2.2` means `>= 1.2.2` and `< 2.0.0`, and `~= 0.4` means `>= 0.4.0` and `< 1.0.0`.
- Release: bump `version` in the .nimble file, commit, tag (`git tag v0.2.0`), push commits and tags. Tags such as `v0.2.0`, `v1` and `foo-1.2.3.4` are recognised.
- Deprecate with the pragma: `{.deprecated.}` or `{.deprecated: "use newProc instead".}`; callers then get a warning (manual).
- Branch on compiler version with `when NimMajor >= 2:` (`NimMajor`, `NimMinor`, `NimPatch` are constants in system).
- `nimble test` compiles and runs `tests/t*.nim`; run it before tagging.
- CI: `jiro4989/setup-nim-action` installs Nim in GitHub Actions (use the version tag from its README, e.g. `@v2`); `iffy/install-nim` (README shows `@v5`) takes a version matrix that can include `devel`. Run `nimble test` in the job.

Gotchas:
- Deprecated symbols still compile; the warning is the only signal.

Verify: `nimble test` is green on the lowest Nim you claim in `requires`.

## Checked

2026-11-03. Confirmed in the Nimble guide (requires operators and `^=`/`~=` examples, release steps, tags, test), manual (`deprecated` pragma), system docs (`NimMajor`) and the setup-nim-action and install-nim READMEs. Removed: the semantic-versioning rule text, `nimble docs` advice, "ORC is the default" claims, and the `1.6.0` example.
Method: documentation only; no commands were run.
