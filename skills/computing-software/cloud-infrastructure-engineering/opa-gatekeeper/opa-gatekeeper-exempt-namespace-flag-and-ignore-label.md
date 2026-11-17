---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-exempt-namespace-flag-and-ignore-label
name: opa-gatekeeper-exempt-namespace-flag-and-ignore-label
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, exempt-namespaces, exempt-namespace, ignore-label, webhook, namespaceselector, helm]
level: advanced
status: docs-checked
description: "Fully bypass the Gatekeeper admission webhook for a namespace with the --exempt-namespace flag plus the admission.gatekeeper.sh/ignore label."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/exempt-namespaces.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper exempt namespace flag and ignore label

To make the API server skip the Gatekeeper webhook entirely for a namespace (for example kube-system), three things must line up:

1. The validating webhook configuration (default `gatekeeper-validating-webhook-configuration`, webhook `validation.gatekeeper.sh`) has this namespaceSelector, already present in the default manifest:

```yaml
namespaceSelector:
  matchExpressions:
    - key: admission.gatekeeper.sh/ignore
      operator: DoesNotExist
```

2. The Gatekeeper pod is started with `--exempt-namespace=<NAME>`. This is deliberate: otherwise permission to label a namespace would equal permission to exempt it from all policy. With Helm, the namespace must be listed in `controllerManager.exemptNamespaces`.
3. The namespace carries the label `admission.gatekeeper.sh/ignore`. Its value is ignored, so it can record the reason.

`--exempt-namespace-prefix` and `--exempt-namespace-suffix` allow whole groups of namespaces. Resources in exempt namespaces are still audited; change constraints or the Config resource to exclude them from audit.

Difference: with the flag and label, the API server never calls Gatekeeper for that namespace, so a Gatekeeper outage has no effect on it. With the Config method the webhook is still called.

## Checked

2026-11-04. Confirmed against exempt-namespaces.md. Removed or corrected: nothing.

Method: documentation only; no commands were run.
