---
id: computing-software.systems-network-administration.restic.feature-flags
name: feature-flags
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, feature-flags, restic-features, alpha, beta, experimental]
level: advanced
status: docs-checked
description: "List and set restic feature flags with restic features and RESTIC_FEATURES, and know what alpha, beta, stable and deprecated mean."
sources:
  - https://restic.readthedocs.io/en/stable/047_tuning_parameters.html
  - https://restic.readthedocs.io/en/stable/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature flags

Some behaviour is controlled by feature flags.

```
restic features
RESTIC_FEATURES=s3-restore restic restore latest
```

`restic features` lists the flags this binary knows with their stage. `RESTIC_FEATURES` takes comma-separated `key[=value]` pairs; the value is `true` (the default if omitted) or `false`.

## Stages

- alpha: off by default; may change or be removed
- beta: on by default; may change slightly or be removed
- stable: always on and cannot be disabled
- deprecated: always off and cannot be enabled; the flag will be removed

An invalid flag name causes an error, and obsolete flags may disappear in a future release. Do not hardcode flags into long-lived scripts without checking them against `restic features` after upgrading.

## Example: S3 Glacier restores

The FAQ shows an alpha-stage restore from cold storage:

```
RESTIC_FEATURES=s3-restore restic restore \
  -o s3.enable-restore=1 -o s3.restore-days=7 -o s3.restore-timeout=24h latest
```

See the faq-cold-storage skill for the caveats.

Treat alpha features as experiments: test restore of real data before depending on them.

## Checked

Checked 2026-11-08 against the restic Tuning parameters page (047_tuning_parameters) and FAQ page (faq), both read in full. Confirmed: RESTIC_FEATURES as a comma-separated key[=value] list with true as the default, the features command listing flags, the alpha, beta, stable and deprecated definitions, errors on invalid flags, possible flag removal, and the s3-restore example. Nothing removed.

Method: documentation only; no commands were run.
