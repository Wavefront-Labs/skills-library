---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-injection-mechanics
name: proxy-injection-mechanics
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, proxy-injection, admission-webhook, annotations]
level: practitioner
status: docs-checked
description: "Control injection with the linkerd.io/inject annotation, know which containers are added and which namespaces are excluded."
sources:
  - https://linkerd.io/2.19/features/proxy-injection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The proxy injector is a Kubernetes admission webhook that adds the proxy to pods when the `linkerd.io/inject: enabled` annotation is present on a namespace or on a workload or pod. It acts no matter whether the pod comes from kubectl, CI/CD or anything else.

Two containers are injected into each pod:

1. `linkerd-init`, an init container that configures iptables to forward all TCP traffic through the proxy. It is omitted when the CNI plugin is enabled.
2. `linkerd-proxy`, the data plane proxy.

Rules:

- Annotating a resource with existing pods does not inject them. Restart them, for example `kubectl rollout restart deploy/my-app`, because Kubernetes only calls the webhook when it creates or updates pods.
- At install time the `kube-system` and `cert-manager` namespaces are excluded from the webhook, and the injector does not run there whatever the annotation says.
- To opt a pod or deployment out when its namespace is injected, set `linkerd.io/inject: disabled`.
- Proxy settings are configured through additional annotations set before injection.

Manual injection: `linkerd inject` is a text transform that adds the annotation to a manifest. With `--manual` it performs the whole injection client-side, which was the default before Linkerd 2.4. Cluster-side injection is preferable because the proxy is always present and configured consistently.

## Checked

2026-11-08. Read in full against the Linkerd 2.19 docs source (markdown in linkerd/website) of https://linkerd.io/2.19/features/proxy-injection/. Confirmed the injected containers, restart rule, excluded namespaces, disable annotation and manual injection notes. Nothing was removed.

Method: documentation only; no commands were run.
