---
id: computing-software.cloud-infrastructure-engineering.google-cloud.scripting-gcloud-non-interactively
name: scripting-gcloud-non-interactively
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gcloud, gcloud-scripting, gcloud-quiet, gcloud-exit-codes, disable-prompts, gcloud-async, gcloud-verbosity, gcloud-log-http, gcloud-in-ci, idempotent-gcloud, gcloud-operations-wait, gcloud-retry]
level: practitioner
status: docs-checked
description: "Write gcloud scripts that survive CI: --quiet and disable_prompts, exit status, --format and --filter for stable output, service account auth, idempotency and retries."
sources: ["https://docs.cloud.google.com/sdk/docs/scripting-gcloud"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scripting gcloud non-interactively

**Goal:** gcloud invocations in bash/CI that never hang on a prompt, fail loudly, and can be rerun
without "already exists" errors.

## 1. No prompts
Disable prompts with the `disable_prompts` property set to True, or per command with the global `--quiet` / `-q`:
```bash
gcloud config set core/disable_prompts true
gcloud compute instances delete vm1 --zone=<Z> --quiet
```
With prompts disabled, the default value of each prompt is used. Pass every required flag
(`--zone`, `--region`, `--project`) explicitly; scripts should not rely on interactive guessing.

## 2. Exit status and output
- Depend on the exit status: non-zero means an error occurred and the output may be incomplete (a command that creates several resources may create only some, list them, and still exit non-zero).
- Do not depend on messages printed to standard error (wording changes between releases) or on the default standard output.
- Use `--format` (json, yaml, csv, text, list, value) and `--filter` to get predictable values, e.g. `--format="value(projectId)"`; `gcloud topic formats` has more.
- `set -euo pipefail` in bash so a pipe does not hide a gcloud failure.
- Parallel execution of multiple gcloud commands is not supported.

## 3. Authorization
User account authorization (`gcloud init`) suits a single machine. Service account authorization is recommended for automation deployed across machines in production: `gcloud auth activate-service-account --key-file [KEY_FILE]`. Prefer keyless options (attached service account or Workload Identity Federation) where available.

## 4. Idempotency
```bash
gcloud compute addresses describe app-ip --region=<R> >/dev/null 2>&1 \
  || gcloud compute addresses create app-ip --region=<R>
```
Prefer update-style commands where they exist; otherwise describe-then-create.

## 5. Long-running operations
Many create commands accept `--async`; check the command's reference page for the flag and for the matching `operations` command group (for example `gcloud sql operations wait`). Note `gcloud compute operations` has no `wait` subcommand (check_commands.py), so use the compute operations reference page to poll.

## 6. Retries
Wrap commands that fail on transient errors in a bounded retry with backoff; do not retry permission or invalid-argument errors.
```bash
retry() { local n=0; until "$@"; do n=$((n+1)); [ $n -ge 5 ] && return 1; sleep $((2**n)); done; }
retry gcloud services enable compute.googleapis.com --project="$P"
```

## Gotchas
- `--quiet` suppresses prompts, not output.
- `gcloud ... list` exits 0 with empty output when nothing matches; test for emptiness.
- Alpha/beta commands change flags between releases; check `gcloud <cmd> --help`.

## Verify
- [ ] Running the script twice succeeds both times.
- [ ] A failing command stops the script with a non-zero exit.

## Checked
2026-10-31. Confirmed on "Scripting gcloud CLI commands": `disable_prompts` and `--quiet`/`-q` with defaults used, exit status guidance, avoid stderr and raw stdout, `--format`/`--filter`, `gcloud auth activate-service-account --key-file`, service account authorization recommendation, no parallel execution. Fixed: the compute operations group has no wait subcommand (check_commands.py). Removed: specific exit code meanings, CLOUDSDK_* environment variables, verbosity and log-http flags, config-dir and component-update advice, Windows note (not on the fetched page).
Method: documentation only; no commands were run.
