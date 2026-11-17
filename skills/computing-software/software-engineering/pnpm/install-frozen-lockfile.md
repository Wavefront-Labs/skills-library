---
id: computing-software.software-engineering.pnpm.install-frozen-lockfile
name: install-frozen-lockfile
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-install, frozen-lockfile, no-frozen-lockfile, prefer-frozen-lockfile, ignore-manifest-check, ci-install]
level: practitioner
status: docs-checked
description: "Control lockfile strictness in pnpm install: --frozen-lockfile defaults, CI behaviour, --no-frozen-lockfile, --prefer-frozen-lockfile, --fix-lockfile and --ignore-manifest-check."
sources:
  - https://pnpm.io/cli/install
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--frozen-lockfile`: pnpm does not write a lockfile and fails if `pnpm-lock.yaml` is missing or out of sync with `package.json`.

Default: false outside CI; true in CI when a lockfile exists. CI is detected with the ci-info rules; `CI=false` turns detection off.

```sh
pnpm install --frozen-lockfile      # strict, reproducible
pnpm install --no-frozen-lockfile   # allow updating in CI
pnpm install --prefer-frozen-lockfile  # reuse lockfile without re-resolving
pnpm install --fix-lockfile         # repair broken lockfile entries
pnpm install --ignore-manifest-check   # skip the manifest-vs-lockfile check
```

- In CI, a lockfile that needs an update makes install fail unless you pass `--no-frozen-lockfile`.
- `--prefer-frozen-lockfile` has the inverse `--no-prefer-frozen-lockfile`, which always re-resolves.
- Use `--ignore-manifest-check` only if you just wrote the lockfile yourself.
- `--force` and `pnpm update` do not bypass integrity checks; see `computing-software.software-engineering.pnpm.install-update-checksums`.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/install: frozen-lockfile semantics and defaults, ci-info detection and CI=false, --no-frozen-lockfile, --prefer-frozen-lockfile and its inverse, --fix-lockfile, --ignore-manifest-check, --force and update not bypassing integrity. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
