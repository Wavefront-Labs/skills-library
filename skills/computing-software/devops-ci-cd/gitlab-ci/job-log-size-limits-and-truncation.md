---
id: computing-software.devops-ci-cd.gitlab-ci.job-log-size-limits-and-truncation
name: job-log-size-limits-and-truncation
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, job-log-limit, log-size-limit, output-limit, log-truncation]
level: practitioner
status: docs-checked
description: "Fix truncated GitLab job logs: the runner output_limit setting, keeping full logs as artifacts, quieting verbose tools, and collapsible sections."
sources: ["https://docs.gitlab.com/runner/configuration/advanced-configuration/", "https://docs.gitlab.com/ci/jobs/job_logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job log size limits and truncation

**Symptom:** the log stops mid-job with a message that the log exceeded its limit; the job
may still fail later, with the failure message invisible.

## 1. The two limits
- **Runner `output_limit`**: maximum build log size in kilobytes, per `[[runners]]`;
  default 4096 (4 MB). The runner admin raises it:
```toml
[[runners]]
  output_limit = 16384
```
- **Instance-level limit** on job log file size: ask your GitLab administrator for the
  value; it was not confirmed in the instance limits page fetched for this review.

## 2. Better: do not stream huge output
```yaml
test:
  script:
    - <your-test-command> > build/test-output.log 2>&1 || (tail -n 200 build/test-output.log; exit 1)
  artifacts:
    when: always
    paths: [build/test-output.log]
    expire_in: 1 week
```
Use each tool's quiet or non-interactive flags (see its own docs). Collapsible sections
(`section_start`/`section_end` markers, or `FF_SCRIPT_SECTIONS` for multi-line scripts)
help reading but do not reduce size.

## 3. Gotchas
- `CI_DEBUG_TRACE: "true"` enables debug logging (tracing): expect much larger logs and
  possibly exposed secrets, so use it only briefly.
- Progress bars that redraw with `\r` can add megabytes; disable them in the tool.
- Once the limit is hit, later output is not collected, so the raw log is also incomplete.

## Verify
- [ ] Full test output is available as an artifact; the job log is under the limit with the failure summary visible.

## Checked

2026-10-28. Confirmed in the GitLab Runner advanced configuration page: `output_limit` is the maximum build log size in kilobytes, default 4096 (4 MB). Confirmed in the GitLab job logs page: section_start/section_end markers and `FF_SCRIPT_SECTIONS`. Confirmed in the predefined variables page: `CI_DEBUG_TRACE` enables debug logging. Removed: the exact truncation message with a byte count, the 100 MB instance default and `ci_jobs_trace_size_limit` (the instance limits page fetched did not document it), the GitLab.com fixed-limit claim, third-party tool quiet flags, and the raw-trace endpoint claim. The Gradle `--console=plain`
example was replaced with a `<your-test-command>` placeholder: no third-party tool flag was
confirmed in the pages fetched for this review.

Method: documentation only; no commands were run.
