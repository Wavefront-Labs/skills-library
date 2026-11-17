---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-default-namespace-context
name: kubectl-default-namespace-context
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, namespace, set-context-namespace, kubens, kubeconfig-contexts, kubectl-config]
level: practitioner
status: docs-checked
description: "Set and verify the default namespace for kubectl (set-context --current --namespace, kubens), and avoid running commands in the wrong namespace or cluster."
sources: ["https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#setting-the-namespace-preference", "https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/", "https://github.com/ahmetb/kubectx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default namespace in the kubectl context

## Set it
```bash
kubectl config set-context --current --namespace=payments
kubectl config view --minify | grep namespace:                      # verify
kubectl config get-contexts                                         # NAMESPACE column
```
With kubectx/kubens (separate tools from github.com/ahmetb/kubectx; also installable as krew
plugins `ctx` and `ns`):
```bash
kubens payments
kubens -          # back to previous namespace
kubectx prod-eu   # switch cluster context
kubectx -         # back to previous cluster
```

## Precedence
1. `--namespace` flag (sets the namespace for that request)
2. namespace in the current context (the "namespace preference")
3. `default`
The Kubernetes docs recommend not using `default` for a production cluster; create and use
other namespaces.

## Safety
- Use separate kubeconfig files per environment and set `KUBECONFIG` per terminal, rather than
  one merged file where switching to prod is a single command away.
- Show the current context and namespace in your shell prompt so you notice a wrong target.
- In scripts always pass `--namespace` and `--context` explicitly; never rely on the current
  context.
- The namespace on a context is only a default; it does not restrict access.

## Per-shell namespace without editing kubeconfig
```bash
alias kp='kubectl -n payments'
```

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Namespaces" (setting the namespace
preference), "Configure Access to Multiple Clusters" and the kubectx README (latest Kubernetes
release v1.37.1). Confirmed: `set-context --current --namespace`, `--namespace` per-request flag,
`default` namespace, `--minify`, `kubens -` and `kubectx -`, krew `ctx`/`ns`. Removed unconfirmed
claims (manifest namespace conflict error, named prompt and shell tools, exam tip).
Method: documentation only; no commands were run.
