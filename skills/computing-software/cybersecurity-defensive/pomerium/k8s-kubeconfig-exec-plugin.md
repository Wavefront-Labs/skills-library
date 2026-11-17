---
id: computing-software.cybersecurity-defensive.pomerium.k8s-kubeconfig-exec-plugin
name: k8s-kubeconfig-exec-plugin
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [kubeconfig, pomerium-cli, exec-credential, kubectl-access, client-authentication]
level: practitioner
status: docs-checked
description: "Point kubectl at a Pomerium route using pomerium-cli as a kubeconfig exec credential plugin."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/kubernetes-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `pomerium-cli` as a credential plugin in `~/.kube/config`:

```yaml
clusters:
  - name: mycluster
    cluster:
      server: https://mycluster.localhost.pomerium.io
users:
  - name: via-pomerium
    user:
      exec:
        apiVersion: client.authentication.k8s.io/v1beta1
        command: pomerium-cli
        args:
          - k8s
          - exec-credential
          - https://mycluster.localhost.pomerium.io
contexts:
  - name: mycluster
    context:
      cluster: mycluster
      user: via-pomerium
current-context: mycluster
```

The cluster `server` is the Pomerium route URL, and the exec argument is the same route URL.
Then bind the user's identity in RBAC (see k8s-rbac-bind-pomerium-users).

## Checked

2026-11-04. Confirmed against the Kubernetes Access page kubeconfig example. Removed a hedging sentence.

Method: documentation only; no commands were run.
