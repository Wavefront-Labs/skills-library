---
id: computing-software.cloud-infrastructure-engineering.linkerd.inject-command-manual-mode
name: inject-command-manual-mode
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, cli, inject, annotations, manual]
level: intro
status: docs-checked
description: "Use linkerd inject to annotate manifests from files or streams, and use --manual only for client-side injection."
sources:
  - https://linkerd.io/2.19/reference/cli/inject/
  - https://linkerd.io/2.19/features/proxy-injection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`linkerd inject` is a text transform. It reads Kubernetes manifests from a file or a stream (`-`) and adds the `linkerd.io/inject: enabled` annotation to eligible resources. When the annotated manifest is applied, the cluster-side proxy injector adds the data plane proxies to the matching pods.

```bash
cat deploy.yml | linkerd inject - | kubectl apply -f -
kubectl -n emojivoto get deploy/voting -o yaml | linkerd inject - | kubectl apply -f -
```

There is no strong reason to use the command in production. The annotation can equally be set by a CI/CD system or any deploy-time mechanism, or placed on a namespace so that every new pod is injected.

`--manual` performs the full injection on the client side. Before Linkerd 2.4 this was the default. Cluster-side injection is easier to keep consistent, so avoid `--manual` unless you cannot use the webhook.

With `--manual` the auto-injector does not pick the pod up, so `config` annotations are not supported.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/reference/cli/inject/, https://linkerd.io/2.19/features/proxy-injection/.

Removed or reworded: Flag/annotation correspondence and rollout-window claims.

Method: documentation only; no commands were run.
