---
id: computing-software.cloud-infrastructure-engineering.terraform.legacy-state-state-out-and-backup-flags
name: legacy-state-state-out-and-backup-flags
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-out-flag, backup-flag, legacy-state-flags, local-backend, state-file]
level: practitioner
status: docs-checked
description: "Understand the legacy -state, -state-out and -backup flags: they apply only to the local backend, how they interact with workspaces, and what the docs recommend instead."
sources: ["https://developer.hashicorp.com/terraform/language/backend/local", "https://developer.hashicorp.com/terraform/cli/commands/apply", "https://developer.hashicorp.com/terraform/cli/commands/state/mv"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legacy `-state`, `-state-out`, `-backup`

## What they are
The local backend page lists them as legacy features kept for backward compatibility and
not recommended. For configurations with a `backend "local"` block, or no backend at all
(which defaults to local), most commands that read or write state accept:

| Flag | Meaning |
|---|---|
| `-state=FILENAME` | overrides the state filename when reading the prior state |
| `-state-out=FILENAME` | overrides the state filename when writing new state |
| `-backup=FILENAME` | overrides the filename the local backend would choose for backups |

- `-state` alone: the same file is used for output, so Terraform overwrites the input
  file when it writes a new snapshot.
- `-state` without `-backup`: the `-state` filename is used as a prefix for the backup
  filename.
- `-backup=-` disables backup files entirely.
- Default state path for the local backend is `terraform.tfstate` relative to the root
  module (`path` setting); `workspace_dir` sets the directory for non-default workspaces.

## The trap
The three options have no effect for configurations that select a different backend
type, so `-state=prod.tfstate` against a remote backend does not target that file.
They were meant for old wrapper scripts that fetched prior state, ran Terraform and saved
the new state, typically using paths in a temp directory.

Setting them also overrides the usual workspace-based state file choice. With all three
set, the selected workspace does not influence which state files are used, so you must
choose distinct filenames yourself to keep workspace states apart.

## Where else the docs mention them
- `terraform apply`: "For configurations using the local backend only, terraform apply
  also accepts the legacy options -state, -state-out, and -backup."
- `terraform state mv`: the local-state form also accepts `-state`, `-state-out`,
  `-backup` and `-backup-out`. Configurations using the remote backend must give a local
  state file with `-state` to use `-backup` and `-backup-out`, which work on local state
  only.

## What to use instead
The docs advise against these options in new systems, even in automation: choose a backend
that supports remote state and configure it in the root module, so everyone retrieves
and stores state in the right shared place without special flags.

## Checked
Date: 2026-11-07
Read in full: local backend (language/backend/local), terraform apply (cli/commands/apply, relevant option text) and terraform state mv (cli/commands/state/mv).
Confirmed: every flag meaning, overwrite and backup-prefix rules, `-backup=-`, workspace interaction, "no effect" for other backends, history of the flags, recommendation, mentions on apply and state mv pages, default path.
Removed: the "ignored or rejected / varies by version" claim (page says no effect), the `terraform apply -state=old -state-out=new` and `state mv` command examples that were not on the pages, the replacement table (workspaces, `state pull`/`push`, `moved`/`removed` blocks, backend versioning, HCP state versions), the "still legitimate" section, and the Verify checklist.
Not opened: other `terraform state` subcommand pages.
Method: documentation only; no commands were run.
