---
id: computing-software.devops-ci-cd.gitlab-runner.runner-instance-executor
name: runner-instance-executor
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [instance-executor, fleeting, nesting, native-steps, maxsessions]
level: advanced
status: docs-checked
description: "Instance executor requirements, nesting and SSH session limits."
sources: ["https://docs.gitlab.com/runner/executors/instance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Instance executor

Generally available since 17.1 (experiment in 15.11, beta in 16.6). It creates instances on demand and runs jobs directly on them, for jobs that need full access to the host OS and devices.

Prepare the environment:
- install a fleeting plugin on the runner manager;
- build a VM image with Git, the GitLab Runner binary in its default path (for artifacts and cache) and your job dependencies. The instances must not register themselves as runners.

Nested virtualization uses the GitLab nesting daemon and is supported only on Apple Silicon instances.

Jobs using the `run` keyword execute as native steps automatically; no feature flag is needed, but the `gitlab-runner` binary must be on the instance `PATH`. Keep it at the manager's version (a mismatch logs a warning). Native steps are not supported on Windows instances.

Each native-steps job opens two concurrent SSH sessions. With `capacity_per_instance` above 1, set `MaxSessions` in `sshd_config` to at least `2 * capacity_per_instance`; the OpenSSH default is 10.

## Checked

2026-11-03. Confirmed against release history, nesting limits, native-steps requirements and the MaxSessions guidance on the Instance executor page.

Method: documentation only; no commands were run.
