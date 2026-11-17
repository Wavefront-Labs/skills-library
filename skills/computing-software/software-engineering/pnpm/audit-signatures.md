---
id: computing-software.software-engineering.pnpm.audit-signatures
name: audit-signatures
category: computing-software
field: software-engineering
product: pnpm
tags: [audit-signatures, registry-signatures, ecdsa-signatures, registry-keys, signature-verification]
level: advanced
status: docs-checked
description: "Verify installed packages' ECDSA registry signatures with pnpm audit signatures against the registry's published keys, including tar integrity targets and exit conditions."
sources:
  - https://pnpm.io/cli/audit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
pnpm audit signatures
pnpm audit signatures --json
```

What it does:
- Verifies the ECDSA registry signature of installed packages against public keys each registry publishes at `/-/npm/v1/keys`.
- Scoped registries from the `registries` setting are respected; registries that publish no signing keys are skipped.
- Signatures are checked against the integrity recorded in the lockfile; a package with no recorded integrity cannot pass.
- A registry signs the integrity of a package's `.tgz`. With `lockfile.integrityTarget: tar`, pnpm verifies against the `.tgz` integrity the registry publishes once it has tied that to the tar hash in the lockfile. The store answers for packages it holds; any other package is downloaded and checked. One that cannot be tied is reported as invalid with the reason.

Exit code 1 when a package has an invalid signature, or when a registry advertises signing keys but a package was published without a signature.

Related: `computing-software.software-engineering.pnpm.audit-vulnerabilities` for advisories and `computing-software.software-engineering.pnpm.lockfile-integrity-and-revisions` for the integrity field.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/audit (signatures section): key endpoint, scoped registries, integrity requirement, integrityTarget tar behaviour, exit code 1 conditions, --json. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
