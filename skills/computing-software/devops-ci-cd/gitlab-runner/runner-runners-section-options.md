---
id: computing-software.devops-ci-cd.gitlab-runner.runner-runners-section-options
name: runner-runners-section-options
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [runners-section, output-limit, pre-build-script, clone-url, unhealthy-requests]
level: practitioner
status: docs-checked
description: "Commonly used options in a [[runners]] section."
sources: ["https://docs.gitlab.com/runner/configuration/advanced-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The [[runners]] section

Key options and defaults:

- `limit`: simultaneous jobs for this runner; `0` (default) means no limit.
- `request_concurrency`: default `1`.
- `strict_check_interval`: when true, disables the faster re-polling loop and strictly respects `check_interval`; default `false`.
- `output_limit`: maximum build log size in kilobytes; default `4096`.
- `prepare_timeout` and `get_sources_timeout`: maximum duration of the prepare and get_sources stages; if unset, zero or above the job timeout, the job timeout applies.
- `unhealthy_requests_limit`: number of unhealthy responses to job requests after which a runner worker is disabled; `unhealthy_interval`: maximum time it stays disabled (`0` never disables).
- `pre_get_sources_script`, `post_get_sources_script`, `pre_build_script`, `post_build_script`: shell snippets run around the job stages.
- `clone_url`: overrides the URL of the GitLab instance; used only if the runner cannot connect to the GitLab URL.
- `api_url`: URL the runner manager uses for GitLab API requests; defaults to `url`.
- `clean_git_config`: cleans the Git configuration.
- `environment`: variables added to every job.

## Checked

2026-11-03. Confirmed against the [[runners]] settings table on Advanced configuration. Removed: invented 19.0 version for the timeouts and the descriptions of unhealthy-request and clone_url behaviour that the page does not state.

Method: documentation only; no commands were run.
