---
id: computing-software.cloud-infrastructure-engineering.istio.istio-revision-tags
name: istio-revision-tags
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, revision-tags, istioctl-tag, default-revision]
level: practitioner
status: docs-checked
description: "Point stable tags like prod-stable at an istiod revision with istioctl tag set, so upgrades need one command instead of relabelling namespaces."
sources: ["https://istio.io/latest/docs/setup/upgrade/canary/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A revision tag is a stable identifier pointing at a revision; namespaces reference it with `istio.io/rev=<tag>`. Repointing the tag moves every namespace labelled with it, with no relabelling.

```sh
istioctl install --revision=1-30-1 --set profile=minimal --skip-confirmation
istioctl install --revision=1-31-3 --set profile=minimal --skip-confirmation
istioctl tag set prod-stable --revision 1-30-1
istioctl tag set prod-canary --revision 1-31-3
kubectl label ns app-ns-1 istio.io/rev=prod-stable
istioctl tag list
istioctl tag set prod-stable --revision 1-31-3 --overwrite
kubectl rollout restart deployment -n app-ns-1
istioctl tag set default --revision 1-31-3
```

Gotchas: restarting the injected workloads is what moves them to the new control plane, so the rollout restart is a separate step. The revision behind the `default` tag injects for `istio-injection=enabled`, `sidecar.istio.io/inject=true` and `istio.io/rev=default`, validates Istio resources, and takes the leader lock to do singleton mesh duties such as updating resource statuses. When using the default tag next to an existing non-revisioned install, remove the old MutatingWebhookConfiguration (typically `istio-sidecar-injector`) so both control planes do not inject. Check mappings with `istioctl proxy-status` (`istioctl ps`) and `istioctl tag list`. Clean up with `istioctl tag remove <tag>`.

## Checked

2026-11-03. Confirmed against the "Stable revision labels" section of the Istio Canary Upgrades guide: tag set/list/remove, overwrite, restart step, default tag semantics and webhook note. Removed: the invented `1-32-0` revision, the claim that new pods report `istio.io/rev` in proxy-status, and the one-tag-per-environment promotion advice.
Method: documentation only; no commands were run.
