---
id: computing-software.devops-ci-cd.nomad.job-dispatch
name: job-dispatch
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, job-dispatch, dispatch, parameterized-job, idempotency-token, id-prefix-template, payload, meta, detach, priority, cli]
level: practitioner
status: docs-checked
description: "Invoke a Nomad parameterized job with nomad job dispatch using payloads up to 16 KiB, -meta, -idempotency-token, -id-prefix-template, -detach, -priority and ACLs."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/job/dispatch.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad job dispatch

Creates an instance of a parameterized job (`computing-software.devops-ci-cd.nomad.parameterized-block`). Each dispatch gets a unique job ID, like `video-encode/dispatch-1485379325-cb38d00d`, that you can track.

```
nomad job dispatch [options] <parameterized job> [input source]
```
The payload comes from a file path or `-` for stdin and is limited to **16384 bytes**.

```
cat config.json | nomad job dispatch video-encode -
nomad job dispatch -meta CAMPAIGN_ID=42 email-blast
nomad job dispatch -detach video-encode video-config.json
```

## Options
- `-meta key=value` - repeatable; merged into the job's metadata, overriding any default. Only keys the parameterized block allows (`meta_required` / `meta_optional`) are accepted, arbitrary keys are rejected.
- `-idempotency-token` - any string; if a dispatch with the same token already exists, nothing new is created and the CLI reports `already dispatched with idempotency token`. Use it to make retries safe.
- `-id-prefix-template` - prefix added to the dispatched job ID.
- `-priority` - integer from 1 to `job_max_priority`, overriding the parent job's priority.
- `-detach` - return the evaluation ID instead of monitoring.
- `-verbose`, `-ui`.

## Exit codes
`0` success, `2` placement problems, `1` any other error.

## ACLs
`dispatch-job` in the namespace; `list-jobs` if you pass a job ID prefix; `read-job` to monitor the evaluation (not needed with `-detach`).

## Gotcha
The parameterized block decides what is accepted: `payload` may be `optional`, `required` or `forbidden`, and keys in `meta_required` must be supplied. The docs point to the multiregion documentation for dispatching in multiregion setups.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 job dispatch command page: usage, 16384 byte payload limit, -meta, -idempotency-token, -id-prefix-template, -priority, -detach, exit codes, ACLs. Removed: the payload-forbidden failure claim (reworded to what the parameterized page states).

Method: documentation only; no commands were run.
