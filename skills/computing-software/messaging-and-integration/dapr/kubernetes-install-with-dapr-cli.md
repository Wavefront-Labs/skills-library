---
id: computing-software.messaging-and-integration.dapr.kubernetes-install-with-dapr-cli
name: kubernetes-install-with-dapr-cli
category: computing-software
field: messaging-and-integration
product: dapr
tags: [kubernetes, dapr-cli, dapr-init, dapr-system, install, mtls]
level: practitioner
status: docs-checked
description: "Install Dapr on Kubernetes with dapr init -k: the dev flag, namespace, HA, disabling mTLS, wait and timeout, private Helm repo environment variables, and Mariner image variant."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Dapr CLI installs the control plane into the cluster in your current kubectl context. Check the target first with `kubectl config get-contexts` (switch with `kubectl config use-context <CONTEXT>`), then run:

```bash
dapr init -k
```

Default namespace is `dapr-system`. Verify with `dapr status -k`; open the dashboard with `dapr dashboard -k` (add `-n <your-namespace>` for a non-default namespace).

Flag variants shown on the page:

- `dapr init -k --dev` adds Redis and Zipkin deployments and applies `statestore`, `pubsub` and an `appconfig` zipkin configuration to the `default` namespace. Development only.
- `dapr init -k --enable-ha=true` runs three replicas of each control plane pod.
- `dapr init -k -n mynamespace` overrides the namespace.
- `dapr init -k --enable-mtls=false` disables mTLS (on by default).
- `dapr init -k --wait --timeout 600` waits for completion; default timeout is 300s.
- `dapr init -k --image-variant mariner` uses Mariner 2 based images instead of the default distroless ones (tags carry a `-mariner` suffix, for example `latest-mariner`).

To pull the chart from a private repository, export these before `dapr init -k`:

```
export DAPR_HELM_REPO_URL="https://helm.custom-domain.com/dapr/dapr"
export DAPR_HELM_REPO_USERNAME="username_xxx"
export DAPR_HELM_REPO_PASSWORD="passwd_xxx"
```

Remove everything with `dapr uninstall -k`. Both the CLI and Helm chart deploy with affinity for nodes labelled `kubernetes.io/os=linux`.

## Checked

Commands and flags confirmed on the Deploy Dapr on a Kubernetes cluster page (CLI tab and Mariner section).

Method: docs-checked 2026-11-09 against raw v1.15 kubernetes-deploy.md (read in full); no commands were run.
