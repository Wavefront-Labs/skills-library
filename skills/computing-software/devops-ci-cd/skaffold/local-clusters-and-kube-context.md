---
id: computing-software.devops-ci-cd.skaffold.local-clusters-and-kube-context
name: local-clusters-and-kube-context
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [local-cluster, minikube, kind, kube-context, docker-desktop]
level: practitioner
status: docs-checked
description: "How Skaffold detects a local cluster, loads images without pushing, how to mark your own context as local, and how the kube-context is chosen."
sources:
  - "https://skaffold.dev/docs/environment/local-cluster/"
  - "https://skaffold.dev/docs/environment/kube-context/"
  - "https://skaffold.dev/docs/design/global-config/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

For supported local clusters such as minikube and Docker Desktop, Skaffold loads images directly into the cluster instead of pushing them to a registry. It detects local clusters from the kubectl context name (see it with `kubectl config current-context`):

- `docker-desktop`, and `docker-for-desktop` (deprecated): Docker Desktop
- `minikube`: minikube. A context can also count as minikube if its cluster certificate is stored at `$HOME/.minikube` or `minikube profile list` returns the context name.
- `kind-(.*)` (kind v0.6.0 and later) and `(.*)@kind` (older kind)
- `k3d-(.*)` (k3d v3.0.0 and later)

Any other name is assumed remote, so images must be pushed.

Manual override for non-standard setups, such as a custom minikube profile: build with the same Docker daemon that runs the pods' containers, and skip pushing either with `build.local.push: false` or by marking the context as local. For `minikube start -p my-profile`:

```bash
source <(minikube docker-env -p my-profile)
skaffold config set --kube-context my-profile local-cluster true
```

Run the first command in the same shell where Skaffold runs.

Caveats from the page:

- Minikube has its own Docker daemon, independent of the host's. Skaffold automatically uses `minikube docker-env` for builders, so built images do not appear in the host's `docker images` unless you configure the Docker CLI with `eval $(minikube docker-env)`.
- Resources with `imagePullPolicy: Always` may fail on local clusters because images are not pushed to a remote registry.

Global config keys `kind-disable-load` and `k3d-disable-load` (boolean) stop Skaffold using `kind load` or `k3d import image` to load images locally.

Choosing the kube-context: by default the current context from your kube-config is used. Override with `--kube-context` or `deploy.kubeContext`; the CLI flag always takes precedence. A running `skaffold dev` session cannot change context; quit and re-run. Profile activation uses the original context, and activating profiles that conflict on context is illegal unless the `--kube-context` flag is given.

Kubeconfig selection: `--kubeconfig` loads only that file; else `$KUBECONFIG` paths are merged; else `${HOME}/.kube/config`. If no kubeconfig is found and neither `--kubeconfig` nor `--kube-context` is given, Skaffold tries an in-cluster configuration from the service account secrets.

## Checked

2026-11-04. Read the Local Cluster page, the whole Kube-context Activation page and the global config table. Confirmed detection list, override steps, caveats, disable-load keys, flag precedence, the dev-session limitation and kubeconfig order. Removed: the `skaffold build --dry-run` tip and the claim that the local flag implies setting a `default-repo` (not on these pages); added the missing `docker-for-desktop` name and minikube certificate rule.
Method: documentation only; no commands were run.
