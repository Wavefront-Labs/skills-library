---
id: computing-software.software-engineering.pnpm.lockfile-integrity-and-revisions
name: lockfile-integrity-and-revisions
category: computing-software
field: software-engineering
product: pnpm
tags: [lockfile-revision, integrity-target, subresource-integrity, tar-registries, lockfile-settings]
level: sme
status: docs-checked
description: "Interpret lockfile integrity and revision fields: revision 0 versus replacements (v12.0.0), what integrity pins, and lockfile.integrityTarget: tar for uncompressed tar hashing."
sources:
  - https://pnpm.io/lockfile
  - https://pnpm.io/cli/update
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Revision (since v12.0.0): a `packages:` entry may carry `revision` beside `integrity`.

```yaml
packages:
  lodash@4.17.21:
    resolution:
      integrity: sha512-<replacement-digest>
      revision: 1
```

It marks a registry revision fetched from `<name>@<version>+r<revision>` rather than the plain `<name>@<version>` URL. `revision: 0` is the original, a positive number a replacement. No `revision` field means an ordinary entry outside the protocol. Tools reading integrity should treat `revision` as ordinary metadata. For a revision, `integrity` pins the uncompressed tar rather than a `.tgz`.

What integrity pins: the resource at its tarball URL after HTTP content decoding, a `.tgz` on most registries, a tar on tar registries. With `lockfile.integrityTarget: tar`, it pins the uncompressed tar of every registry package, `tarball:` URL and `file:` tarball, and the lockfile records:

```yaml
settings:
  autoInstallPeers: true
  excludeLinksFromLockfile: false
  integrityTarget: tar
```

To refresh integrity after a registry rewrites tarballs, see `computing-software.software-engineering.pnpm.install-update-checksums`; to refresh revisions use `pnpm update --patches`.

## Checked

2026-11-04. Confirmed against pnpm.io/lockfile and pnpm.io/cli/update: revision field semantics (v12.0.0), integrity target and tar settings block, update --patches refreshing registry revisions. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
