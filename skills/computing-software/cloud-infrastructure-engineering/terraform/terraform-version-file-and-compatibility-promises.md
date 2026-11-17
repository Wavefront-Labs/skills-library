---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-version-file-and-compatibility-promises
name: terraform-version-file-and-compatibility-promises
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, terraform-version-file, compatibility-promises, tfenv, tenv, required-version, state-format, version-pinning]
level: practitioner
status: docs-checked
description: "Pin the Terraform CLI per repo with .terraform-version (tfenv) and know what the 1.x compatibility promises cover, including state downgrades."
sources: ["https://developer.hashicorp.com/terraform/language/v1-compatibility-promises", "https://github.com/tfutils/tfenv", "https://developer.hashicorp.com/terraform/language/terraform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .terraform-version and the 1.x compatibility promises

## Pinning the CLI
```
# .terraform-version (repo root)
1.9.8
```
- tfenv reads it: `tfenv install` with no argument installs the version in the file, and
  `TFENV_TERRAFORM_VERSION` overrides it. tfenv also accepts `latest:<regex>` and
  `min-required` (scans your Terraform files for the minimum `required_version`).
- Other version managers (tenv, asdf, mise) have their own file conventions: check each
  tool's README before relying on `.terraform-version`.
- CI: read the file and pass its value to whatever installs Terraform, so CI and
  developers cannot drift.
- HCP Terraform: set the workspace Terraform version to match.

Keep `required_version` in code as the guard rail (Terraform errors and exits when the
running version does not satisfy it) and `.terraform-version` as the exact pin; bump both
in one PR.

## What the 1.x promises cover
- **Configuration language**: modules written for 1.0 are intended to keep planning and
  applying through 1.x. Excepted: invalid configurations, experimental features, security
  fixes, and fixes where behaviour differed from the documentation.
- **Upgrade and downgrade**: upgrading from any 1.x to any later 1.x is intended to work.
  Downgrading is not guaranteed: later releases may add new state snapshot formats. Once a
  newer version writes state, older CLIs may not read it.
- **Protected workflow commands**: the page lists the `init`, `validate`, `plan`, `apply`,
  `show`, `fmt`, `output`, `force-unlock`, `state` (some) and other commands and flags it
  will not break. Automation should rely only on `-json`/`-raw` output and exit codes;
  human-readable output is not a stable interface. `destroy`, `console`, `graph`,
  `import`, `refresh`, `state mv|rm|replace-provider` and `workspace` are listed as
  commands that might change.
- **Provider protocol**: protocol version 5 is supported throughout 1.x. Providers
  themselves are not covered and can change independently.
- **Backends**: only `local` and `http` are covered; `gcs` is maintained by outside
  contributors and is not covered.
- **Not covered**: experimental features, HCP Terraform, providers, external modules.

## Upgrade practice
Upgrade all writers of a state together (CI images, developers, HCP workspace); otherwise
the first newer apply may lock out everyone still on the old version.

## Verify
- [ ] `terraform version` in CI equals `.terraform-version`.
- [ ] All workspaces/CI jobs for a state upgraded in the same change window.

## Checked
Date: 2026-10-28.
Confirmed in the Terraform v1.x Compatibility Promises page: language promise and its
exceptions, upgrade/downgrade wording, protected workflow commands, commands that might
change, provider protocol 5, backend coverage. Confirmed in the tfenv README:
`.terraform-version`, `TFENV_TERRAFORM_VERSION`, `latest:<regex>`, `min-required`.
Confirmed in the terraform block reference: `required_version` errors when unmet.
Removed as unconfirmed: asdf `.tool-versions`, the setup-terraform CI snippet, the
`latest:^1.9` example, the quoted state-snapshot error text, plan-file and `.terraform/`
layout claims, plan JSON `format_version` claim.
Method: documentation only; no commands were run.
