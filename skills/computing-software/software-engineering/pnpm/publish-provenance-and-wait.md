---
id: computing-software.software-engineering.pnpm.publish-provenance-and-wait
name: publish-provenance-and-wait
category: computing-software
field: software-engineering
product: pnpm
tags: [provenance, trusted-publishing, publish-wait-timeout, batch-publish, report-summary-publish, skip-manifest-obfuscation]
level: advanced
status: docs-checked
description: "Release hardening for pnpm publish: --provenance and trusted publishing, --publish-wait-timeout (v12.7.0), --batch publishing, publish summaries and manifest obfuscation."
sources:
  - https://pnpm.io/cli/publish
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Provenance: from a supported cloud CI the package is publicly linked to where it was built. Under trusted publishing pnpm attaches provenance to a public package from a public repo on its own. Opt out with `--no-provenance` (or `--provenance=false`), e.g. on a self-hosted runner. Setting `provenance` (or `PNPM_CONFIG_PROVENANCE`) sets the default; CLI wins.

Wait for availability (v12.7.0): `--publish-wait-timeout <ms>` (default 0, off; setting `publishWaitTimeout`, env `PNPM_CONFIG_PUBLISH_WAIT_TIMEOUT`) waits for the exact version to appear in install metadata, then expects HTTP 200 on a HEAD of its tarball URL. Timeout per package; with `--batch` per registry group.

```sh
pnpm -r publish --publish-wait-timeout 600000 --report-summary
```

- Recursive publishing checks already-existing selected versions and confirms availability before publishing dependents.
- Timeout gives `ERR_PNPM_PUBLISH_AVAILABILITY_TIMEOUT`: the upload remains accepted, do not publish that version again. Non-retryable errors give `ERR_PNPM_PUBLISH_AVAILABILITY_CHECK_FAILED`.
- `--dry-run` skips the check; the check does not verify archive contents.

`--batch`: send all packages in one `PUT /-/pnpr/v0/publish`; registry must support it (`ERR_PNPM_BATCH_PUBLISH_UNSUPPORTED`). All-or-nothing, grouped per registry, one credential per group.

`--report-summary` writes `pnpm-publish-summary.json` (`publishedPackages` with name and version), even after a partial failure. `--skip-manifest-obfuscation` keeps `packageManager` and publish scripts in the manifest.

## Checked

2026-11-04. Confirmed provenance and trusted publishing behaviour, --publish-wait-timeout (v12.7.0) semantics and error codes, --batch, --report-summary and --skip-manifest-obfuscation against pnpm.io/cli/publish. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
