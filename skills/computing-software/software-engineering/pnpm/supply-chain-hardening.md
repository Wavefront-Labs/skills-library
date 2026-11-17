---
id: computing-software.software-engineering.pnpm.supply-chain-hardening
name: supply-chain-hardening
category: computing-software
field: software-engineering
product: pnpm
tags: [supply-chain-security, allow-builds, strict-dep-builds, block-exotic-subdeps, trust-policy, named-registries, lockfile-commit]
level: practitioner
status: docs-checked
description: "Reduce npm supply-chain risk with pnpm: allowBuilds, strictDepBuilds, blockExoticSubdeps, minimumReleaseAge, trustPolicy and its excludes, committed lockfiles, named registries."
sources:
  - https://pnpm.io/supply-chain-security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defences, in the order the docs give them:

1. Build scripts: dependency build scripts do not run unless listed in `allowBuilds`. `strictDepBuilds` (on by default) makes an install fail when a dependency has a build script not allowed. `dangerouslyAllowAllBuilds` re-enables everything globally; list only trusted dependencies instead. Be careful updating a trusted package that has a `postinstall`.
2. Exotic subdependencies: `blockExoticSubdeps` (on by default) stops transitive dependencies from git repositories or direct tarball URLs.
3. Delay: `minimumReleaseAge` in minutes, default `1440` (1 day); `0` opts out; `10080` waits a week.
4. Trust: `trustPolicy: no-downgrade` blocks a package whose trust level dropped versus earlier releases (e.g. trusted publisher before, only provenance or nothing now). `trustPolicyExclude` bypasses named packages or versions. `trustPolicyIgnoreAfter` skips trust checks for versions published longer ago than a threshold.
5. Lockfile: always commit it. When scanning `pnpm-lock.yaml`, handle the two-document form (`computing-software.software-engineering.pnpm.lockfile-reading-documents`).
6. Registries: for packages that must come from a specific registry use `namedRegistries` aliases; the lockfile keys become `<name>@<registryName>:<version>` so another registry cannot substitute the same name and version.

## Checked

2026-11-04. Confirmed allowBuilds and strictDepBuilds, blockExoticSubdeps, minimumReleaseAge default and examples, trustPolicy and its excludes, the lockfile advice and named registry keys against pnpm.io/supply-chain-security. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
