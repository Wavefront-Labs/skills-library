---
id: computing-software.devops-ci-cd.concourse-ci.task-step-security-and-resource-limits
name: task-step-security-and-resource-limits
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [task-step, privileged, hermetic, container-limits, cpu-shares, memory, security]
level: advanced
status: docs-checked
description: "Restrict or widen a task container: privileged and why it is not in the task file, hermetic no-network mode (containerd only), and container_limits CPU shares and memory bytes."
sources:
  - https://concourse-ci.org/docs/steps/task/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three task step fields change the container's power.

**`privileged`** (default `false`). Gives the task escalated capabilities. The page calls it a gaping security hole. It is a step field and not part of the task config on purpose, so a pull request that edits the task file cannot escalate privilege. On Linux it decides whether the container runs in a separate user namespace; when `true`, the container's `root` is real root. Never use it with code you do not trust, such as pull requests. It has no effect on macOS or Windows, where workloads are not containerized.

**`hermetic`** (default `false`). When `true`, the task has no outbound network access: it cannot reach the internet or local network resources outside the container. Supported only by the `containerd` runtime on Linux; on other runtimes it has no effect on networking, so ask your operator which runtime is in use. No effect on macOS or Windows.

**`container_limits`** takes `cpu` and `memory`. CPU is measured in shares relative to other containers on the worker (two containers of 2 shares each get 50% each; add a 4-share container and they get 25%, 25%, 50%). Memory is in bytes. 0 means unlimited. Step-level limits override both the task config's `container_limits` and the web node's `--default-task-cpu-limit` and `--default-task-memory-limit`.

```yaml
- task: constrained-task
  container_limits:
    cpu: 2
    memory: 10000000
```

## Checked

Checked 2026-11-09 against the raw docs source of the Task Step page (read in full): defaults, warnings, the containerd restriction, override order and the CPU share arithmetic all match.

Method: docs-checked 2026-11-09 against concourse docs task step page (github.com/concourse/docs source); documentation only, no commands were run.
