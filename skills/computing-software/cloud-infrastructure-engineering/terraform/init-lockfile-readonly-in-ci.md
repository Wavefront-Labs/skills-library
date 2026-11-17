---
id: computing-software.cloud-infrastructure-engineering.terraform.init-lockfile-readonly-in-ci
name: init-lockfile-readonly-in-ci
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, lockfile-readonly, terraform-init, dependency-lock, ci-cd, supply-chain]
level: practitioner
status: docs-checked
description: "Use terraform init -lockfile=readonly in CI so pipelines verify provider checksums without changing .terraform.lock.hcl, and how to keep the lock file complete across platforms."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/init#lockfile-mode", "https://developer.hashicorp.com/terraform/language/files/dependency-lock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `init -lockfile=readonly`

## What the lock file does
`.terraform.lock.hcl` sits in the working directory (the root module's directory) and
records the provider versions Terraform selected. It tracks only providers, not modules;
for modules use exact version constraints if you need the same selection every time.
Plain `terraform init` creates or updates it: a provider with no recorded selection gets
the newest version matching the constraint and the file is updated, while a recorded
selection is always re-selected even if a newer version exists. `-upgrade` makes
Terraform ignore recorded selections. Commit the file so changes go through code review.

## The flag
```bash
terraform init -input=false -lockfile=readonly
```
`-lockfile=readonly` suppresses lock file changes but still verifies checksums against
what is already recorded. It conflicts with `-upgrade`. `-input=false` makes init error
instead of prompting for input.

Checksum verification: if an installed package matches none of the recorded checksums,
init fails ("Failed to install provider ... doesn't match any of the checksums
previously recorded in the dependency lock file"). This is a trust-on-first-use model.

## Keeping the file complete for CI
- Registry installs record signed checksums for all platforms, so the lock file is
  usually usable elsewhere. Installing first from a filesystem or network mirror records
  checksums only for the platform where init ran, and the configuration then will not
  verify on other platforms.
- Fix: pre-populate with `terraform providers lock`, one `-platform` per target:
```bash
terraform providers lock -platform=linux_arm64 -platform=linux_amd64 \
  -platform=darwin_amd64 -platform=windows_amd64
```
  This downloads and verifies the official packages and records both `zh:` and `h1:`
  checksums.
- Terraform may add `h1:` hashes later when you run on a new platform; pre-populating
  avoids those incremental diffs.

## Making a change on purpose
Run `terraform init -upgrade` outside the readonly CI step, review the lock file diff
(version, constraints, hashes) and commit it. A new provider requirement creates a new
`provider` block in the lock file; removing the last use of a provider from both
configuration and state makes init remove its entry.

## Other pipeline note
`-plugin-dir=PATH` forces plugins to be read only from that directory, as if it were a
`filesystem_mirror`; the docs recommend a global CLI configuration for routine mirror
use. The init page points to the "Running Terraform in Automation" tutorial for
pipeline guidance.

## Checked
Date: 2026-11-07
Read in full: terraform init command (cli/commands/init, including Plugin Installation and the lockfile option) and Dependency Lock File (language/files/dependency-lock, including the checksum verification and diff sections).
Confirmed: readonly semantics and the -upgrade conflict; -input=false behaviour; lock file location, name, providers-only scope and commit advice; selection and -upgrade behaviour; checksum mismatch error; mirror caveat; providers lock -platform example; removal of unused entries; -plugin-dir.
Removed: the error-and-fix table (the pages do not list readonly-mode error messages, so the "no record of provider" and "does not match configured version constraint" strings are unconfirmed), "do not commit the lock file for reusable modules", the claim that CI pins "vanish with the runner", the `git status --porcelain` Verify step, and the Verify checklist.
Not opened: the terraform providers lock command page and the Running Terraform in Automation tutorial.
Method: documentation only; no commands were run.
