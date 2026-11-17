---
id: computing-software.systems-network-administration.restic.self-update-binary
name: self-update-binary
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, self-update, binary, checksum, github-token]
level: intro
status: docs-checked
description: "Update a restic binary in place with restic self-update, save the result elsewhere with --output, and avoid GitHub rate limits."
sources:
  - https://restic.readthedocs.io/en/stable/020_installation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update restic with self-update

An official binary can replace itself:

```
restic version
restic self-update
```

`self-update` finds the latest release at GitHub, downloads `SHA256SUMS` and its signature, verifies the GPG signature and replaces the binary. It needs restic 0.9.3 or later, and the user running it must have permission to replace the binary. Use `--output` to save the downloaded binary to a different file.

## Rate limits

Set a personal access token in `GITHUB_ACCESS_TOKEN` to raise the rate limit through authenticated GitHub API requests; this prevents update failures when many unauthenticated requests came from the same IP.

## When not to use it

- Package-managed installs: the docs describe `self-update` for official binaries, so update packaged installs through the package manager.

## Verifying downloads by hand

Release assets are accompanied by `SHA256SUMS` and a detached signature `SHA256SUMS.asc`. The signing key id given in the installation docs is `0x91A6868BD3F7A907`. Check the signature on the checksum file, then check the binary against the checksum file.

## Checked

2026-11-03. Confirmed in the restic docs page Installation (Packages intro, Official binaries): `self-update` for official binaries, the 0.9.3 requirement, GPG verification, `--output`, `GITHUB_ACCESS_TOKEN`, `SHA256SUMS`/`SHA256SUMS.asc` and key `0x91A6868BD3F7A907`. Removed: the setcap capability claim and the multi-host version advice (not in the docs).

Method: documentation only; no commands were run.
