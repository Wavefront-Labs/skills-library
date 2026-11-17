---
id: computing-software.devops-ci-cd.nomad.periodic-block
name: periodic-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, periodic-job, periodic, cron, crons, prohibit-overlap, time-zone, batch, sysbatch, distributed-cron, hcl]
level: practitioner
status: docs-checked
description: "Schedule Nomad periodic jobs with the periodic block using cron or crons, prohibit_overlap, time_zone and enabled, plus the batch-only rule and daylight saving behaviour."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/periodic.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad periodic block (periodic-job)

`periodic` makes a job run on a schedule, a "distributed cron". Expressions evaluate in **UTC** by default.

```hcl
job "docs" {
  type = "batch"
  periodic {
    crons            = ["*/15 * * * * *", "@daily"]
    prohibit_overlap = true
    time_zone        = "UTC"
  }
}
```

## Requirements
- Job `type` must be `batch` or `sysbatch`.
- An existing job cannot be updated into a periodic job. First run `nomad stop -purge <job>`, then submit the periodic version; this is deliberate so the change is intentional.

## Parameters
- `crons` - list of cron expressions; the job runs at the next earliest time matching any. Predefined forms like `@daily` and `@weekly` work.
- `cron` - deprecated single-expression form, replaced by `crons` in 1.6.2. Set either `cron` or `crons`, never both.
- `prohibit_overlap` (`false`) - wait for previous instances of this job to finish; it does not serialise against other periodic jobs.
- `time_zone` (`"UTC"`) - must be parseable by Go `time.LoadLocation`.
- `enabled` (`true`) - when `false` the job does not run on schedule and forced launches are also blocked.

## Daylight saving
The docs recommend leaving UTC. With a local zone such as `America/New_York`: a run scheduled in the skipped spring-forward hour (2:30am) is skipped that day; a run in the repeated fall-back hour (1:30am) runs twice.

## Related
- Combining with `parameterized` follows `parameterized => periodic => batch`; see `computing-software.devops-ci-cd.nomad.parameterized-block`.
- Force a run with `nomad job periodic force <job>` (a disabled job cannot be forced).
- The docs point to the multiregion documentation for extra time-zone considerations.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 periodic job specification page and the parameterized page for periodic force: batch and sysbatch requirement, nomad stop -purge, cron deprecation in 1.6.2, crons, prohibit_overlap, time_zone, enabled, daylight saving behaviour, parameterized with periodic. Removed: the cronexpr library claim and a five-field example expression the page does not show.

Method: documentation only; no commands were run.
