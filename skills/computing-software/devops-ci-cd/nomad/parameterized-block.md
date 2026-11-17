---
id: computing-software.devops-ci-cd.nomad.parameterized-block
name: parameterized-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, parameterized-job, parameterized, dispatch-payload, meta-required, meta-optional, payload, batch, sysbatch, nomad-meta, hcl]
level: practitioner
status: docs-checked
description: "Define Nomad parameterized batch jobs that act like functions, with payload required optional or forbidden, meta_required, meta_optional and dispatch_payload files."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/parameterized.mdx", "https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/dispatch_payload.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad parameterized block (parameterized-job)

A job with a `parameterized` block is a template: it does nothing until invoked with `nomad job dispatch` (or the HTTP API), which creates a child job with its own unique ID (tracked like a future). The job type must be `batch` or `sysbatch`. A dispatched child cannot be edited; change the parent instead.

```hcl
job "video-encode" {
  type = "batch"
  parameterized {
    payload       = "required"
    meta_required = ["dispatcher_email"]
    meta_optional = ["pager_email"]
  }
  group "encode" {
    task "ffmpeg" {
      driver = "exec"
      config {
        command = "ffmpeg-wrapper"
        args    = ["-config=${NOMAD_TASK_DIR}/config.json"]
      }
      dispatch_payload {
        file = "config.json"
      }
    }
  }
}
```

## Parameters
- `payload` (`"optional"`) - `"optional"`, `"required"` or `"forbidden"`. **Maximum payload size is 16 KiB.**
- `meta_required` - keys that must be given at dispatch.
- `meta_optional` - keys that may be given.

## Getting inputs into tasks
- `dispatch_payload { file = "..." }` in a task writes the payload to that file, relative to the task's local directory, before the task starts.
- Metadata is exposed as environment interpolation, for example `${NOMAD_META_CAMPAIGN_ID}` in `args`.

## With periodic
When a job has both blocks, the parameterized one wins: the periodic schedule does not start until someone dispatches. Each dispatch child then launches periodic grandchildren using that dispatch's parameters. IDs look like `sync/dispatch-<ts>-<id>/periodic-<ts>`. To force a run, force the dispatched child: `nomad job periodic force sync/dispatch-<ts>-<id>`.

See `computing-software.devops-ci-cd.nomad.job-dispatch` for the CLI side.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 parameterized and dispatch_payload job specification pages: batch and sysbatch requirement, payload values and 16 KiB limit, meta_required and meta_optional, dispatch_payload file path, meta interpolation, periodic combination and force. Nothing removed.

Method: documentation only; no commands were run.
