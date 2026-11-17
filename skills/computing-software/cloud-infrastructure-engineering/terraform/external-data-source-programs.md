---
id: computing-software.cloud-infrastructure-engineering.terraform.external-data-source-programs
name: external-data-source-programs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, external-data-source, external-program, hashicorp-external, json-protocol, escape-hatch]
level: advanced
status: verified
description: "Use the external data source safely: the JSON stdin/stdout protocol, string-only results, error handling, portability, and when to write a provider instead."
sources: ["https://registry.terraform.io/providers/hashicorp/external/latest/docs/data-sources/external"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The `external` data source

Runs a local program at **plan time** and turns its JSON output into attributes.

## Protocol
- Terraform writes the `query` map as a JSON object to the program's **stdin**.
- The program prints a JSON object of **string → string** to stdout and exits 0.
- Non-zero exit = error (`External Program Execution Failed`); stderr is shown as the error message with `exit status N`.

```hcl
data "external" "git" {
  program = ["bash", "${path.module}/scripts/git-info.sh"]
  query = {
    dir = path.root
  }
}
locals {
  git_sha = data.external.git.result.sha
}
```
```bash
#!/usr/bin/env bash
set -euo pipefail
eval "$(jq -r '@sh "DIR=\(.dir)"')"          # safe parsing of stdin
SHA=$(git -C "$DIR" rev-parse --short HEAD)
BRANCH=$(git -C "$DIR" rev-parse --abbrev-ref HEAD)
jq -n --arg sha "$SHA" --arg branch "$BRANCH" '{sha: $sha, branch: $branch}'
```

## Rules
- Values must be strings: numbers/bools/lists → `Error: Unexpected External Program Results` (`json: cannot unmarshal number into Go value of type string`, ran with provider 2.4.2).
  Encode complex values as a JSON string and `jsondecode()` them in HCL.
- Runs on every plan, on whatever machine runs Terraform (CI runner, remote worker):
  it needs the interpreter and tools there (`jq`, `git`), so install them on every runner.
- Must be idempotent and side-effect free (it runs during plan, possibly many times).
- Program path is relative to the working directory (ran: `scripts/cwd.sh` resolved from the root, and the program saw the root as its cwd) — always use `${path.module}`. The `working_dir` argument (provider 2.4.2) sets the program's cwd (ran: `working_dir = "sub"` printed `.../sub`).

## When not to use it
- Fetching from an HTTP API → `http` data source.
- Reading files → `file()`, `local_file`.
- Anything needing create/update/delete lifecycle → write a provider (Plugin Framework)
  or a `terraform_data` + provisioner.

## Gotchas
- Windows: `program = ["bash", ...]` worked here because Git Bash is on PATH; on a machine without it the program fails to start, so pick an interpreter that is installed on every runner.
- Results are stored in state (strings in plaintext) — not for secrets.
- Unknown `query` values (from resources being created) defer the read to apply.

## Verify
- [ ] `echo '{"dir":"."}' | bash scripts/git-info.sh` prints a flat JSON string map.
- [ ] `terraform console` → `data.external.git.result` shows the expected keys.

## Checked
- Terraform 1.17.0, hashicorp/external 2.4.2, Git Bash with jq 1.7.1: the git-info script ran from `terraform apply` and returned `{branch, sha}` as a map of strings, and standalone with `echo '{"dir":"."}' | bash scripts/git-info.sh`; a program printing a number and a bool failed with the quoted error; exit 3 with stderr text produced `External Program Execution Failed`; unknown `query` value gave `will be read during apply (config refers to values not yet known)`; relative program path and `working_dir` behaviour measured.
- Not exercised: other runner images and Windows hosts without Git Bash (the skill only says the interpreter must exist there). The earlier plan output showed the stored result (`- sha = "cef1b5f"`), confirming results live in state.
