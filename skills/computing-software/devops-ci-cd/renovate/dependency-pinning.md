---
id: computing-software.devops-ci-cd.renovate.dependency-pinning
name: dependency-pinning
category: computing-software
field: devops-ci-cd
product: renovate
tags: [pinning, pin-dependencies, reproducible-builds, renovate]
level: practitioner
status: docs-checked
description: "Why and how to pin dependency versions with Renovate, and the trade-off between apps and libraries."
sources:
  - https://docs.renovatebot.com/dependency-pinning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Pinning means declaring an exact version rather than a range. The Renovate docs argue that unpinned ranges let an upstream release change your build without any commit in your repo, which makes failures hard to trace. With pinned versions, each change appears as a Renovate PR, tested before it merges, and rollbacks are clean.

The trade-offs:

- Applications benefit most from pinning, since nobody consumes their ranges.
- Browser or dual browser/Node.js libraries consumed by others should keep SemVer ranges for dependencies, and can pin `devDependencies`. Node.js-only libraries can consider pinning everything, unless the library is a micro one likely to be used in disk-sensitive environments.
- Pinning produces an initial "Pin Dependencies" PR, then one PR per update, so expect more PRs.

```json
{
  "rangeStrategy": "pin"
}
```

To control the extra volume, add Renovate rules for scheduling, grouping or automerging safe updates.

Use a lock file whether or not you pin: a lock file pins deeper into the tree, while pinning makes each direct dependency change visible as a PR. The docs recommend a lock file regardless, and pinning even if you have one.

## Checked

2026-11-03. Confirmed against the Renovate "Should you Pin your JavaScript Dependencies?" page (recommendations for apps and libraries, noise trade-off, lock files) and the configuration options page (`rangeStrategy` `pin`, the "Pin Dependencies" PR). Removed: the `config:best-practices` extends line and the claim about PR titles and closed-PR matching in this context.

Method: documentation only; no commands were run.
