---
id: computing-software.devops-ci-cd.flux.gitrepository-ref-and-verification
name: gitrepository-ref-and-verification
category: computing-software
field: devops-ci-cd
product: flux
tags: [gitrepository, ref, semver, verify, signatures]
level: sme
status: docs-checked
description: "Pin a GitRepository to a branch, tag, semver range, named ref or commit, and verify commit or tag signatures."
sources:
  - https://fluxcd.io/flux/components/source/gitrepositories/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.ref` takes `branch`, `tag`, `semver`, `name` and `commit`; later fields in that list win. If unset, it defaults to the `master` branch, so set the branch explicitly when yours is `main`.

```yaml
spec:
  ref:
    branch: main
```

- `branch`: shallow clone of that branch.
- `tag`: a specific tag.
- `semver`: a range such as `">=1.0.0 <2.0.0"` resolved against tags.
- `name`: a full ref like `refs/heads/main`, `refs/tags/v0.1.0`, `refs/pull/420/head`, `refs/merge-requests/1/head`.
- `commit`: pin to a SHA.

Verification with `.spec.verify`:
- `mode`: `HEAD` (commit at HEAD after checkout), `Tag` (the tag object from `ref.tag`, `ref.semver` or `ref.name`), or `TagAndHEAD` (the tag and the commit it points to). `head` is accepted for backward compatibility.
- `secretRef.name`: Secret holding trusted public keys. PGP keys need an `.asc` key suffix, SSH keys `.sshpub`; unsuffixed keys are treated as PGP key rings.

```yaml
spec:
  verify:
    mode: HEAD
    secretRef:
      name: pgp-public-keys
```

A failed verification adds a failure condition to the GitRepository. The controller records a fingerprint of the trusted keys in `.status.sourceVerificationFingerprint`; PGP success messages report the key ID and SSH ones the SHA256 fingerprint.

## Checked

2026-11-03. Read the GitRepository reference (fluxcd.io/flux/components/source/gitrepositories/): `.spec.ref` fields and precedence, `master` default, `refs/...` examples, verification modes, `.asc` and `.sshpub` key suffixes, and `.status.sourceVerificationFingerprint`. Removed an unsupported pinning recommendation and an unsupported failure consequence.

Method: documentation only; no commands were run.
