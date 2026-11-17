---
id: computing-software.devops-ci-cd.gitlab-runner.runner-install-helm-chart
name: runner-install-helm-chart
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [install, kubernetes, helm, rbac, values-yaml]
level: practitioner
status: docs-checked
description: "Deploy GitLab Runner into a cluster with the official Helm chart and its required values."
sources: ["https://docs.gitlab.com/runner/install/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install with the Helm chart

The chart runs GitLab Runner with the Kubernetes executor and provisions a new pod in the specified namespace for each CI/CD job.

Required values in `values.yaml`:
- `gitlabUrl`: full URL of the GitLab server, such as `https://gitlab.example.com`.
- `rbac: { create: true }`: creates RBAC rules for the runner to create pods that run jobs.
- `runnerToken`: the authentication token from the GitLab UI. Set it directly or store it in a secret.

By default `rbac.rules` is empty and the chart grants the service account all verbs on all resources in the core API group. To use an existing service account, set `rbac.create: false` and `serviceAccount.create: false` and give your existing service account name in the values.

Install:
```
helm repo add gitlab https://charts.gitlab.io
helm search repo -l gitlab/gitlab-runner
helm install --namespace <NAMESPACE> gitlab-runner -f <CONFIG_VALUES_FILE> gitlab/gitlab-runner
```
If the latest versions are not listed, run `helm repo update gitlab`. The GitLab API must be reachable from the cluster.

## Checked

2026-11-03. Confirmed against required values, default RBAC rules, helm commands and the API-reachability prerequisite on Install on Kubernetes. Corrected the service account instruction.

Method: documentation only; no commands were run.
