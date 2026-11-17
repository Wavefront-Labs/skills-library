---
id: computing-software.cloud-infrastructure-engineering.linkerd.linkerd-check-health
name: linkerd-check-health
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, cli, check, health, troubleshooting]
level: intro
status: docs-checked
description: "Run linkerd check, with --proxy for data plane skew, as the first health step before and after changes."
sources:
  - https://linkerd.io/2.19/reference/cli/check/
  - https://linkerd.io/2.19/tasks/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`linkerd check` validates the CLI, cluster and control plane. Its output is grouped into sections:

- `kubernetes-api` and `kubernetes-version`: the client can reach the cluster and the Kubernetes version meets the minimum
- `linkerd-existence`: the control plane namespace exists, the controller pod runs, the control plane API can be queried
- `linkerd-api`: control plane pods are ready and can talk to Kubernetes and Prometheus
- `linkerd-service-profile`: no invalid service profiles
- `linkerd-version` and `control-plane-version`: the CLI and control plane are up to date and their versions match

A healthy run ends with `Status check results are √`. Each failed check prints a hint and a link into the troubleshooting guide, which lists every possible check, what it does and how to fix it.

```bash
linkerd check
linkerd check --proxy
```

Use `--proxy` to include data plane checks; after a data plane upgrade it lists any pods still running older proxy versions.

Use it as the gate in workflows: before an upgrade and after the control plane upgrade. For a major version upgrade also run `linkerd check --proxy` first to catch unintended version skew.

## Checked

2026-11-08. Read in full against the Linkerd 2.19 docs source (markdown in linkerd/website) of https://linkerd.io/2.19/reference/cli/check/ (command flags are generated and were not available) and https://linkerd.io/2.19/tasks/upgrade/. Confirmed the output sections and the use of check and check --proxy around upgrades. Removed unsourced claims about expired-certificate checks and extension sections.

Method: documentation only; no commands were run.
