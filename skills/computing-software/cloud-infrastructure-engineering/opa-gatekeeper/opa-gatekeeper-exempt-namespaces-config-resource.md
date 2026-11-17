---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-exempt-namespaces-config-resource
name: opa-gatekeeper-exempt-namespaces-config-resource
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, exempt-namespaces, config, excludednamespaces, processes, wildcard]
level: practitioner
status: docs-checked
description: "Exclude namespaces from audit, webhook, sync or mutation-webhook processing cluster-wide using the Gatekeeper Config resource."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/exempt-namespaces.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper exempt namespaces config resource

The Config resource (alpha, must be named `config`; the doc example places it in `gatekeeper-system`) can exclude namespaces from specific Gatekeeper processes for all constraints. Asterisk wildcards such as `kube-*` are allowed.

```yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: "gatekeeper-system"
spec:
  match:
    - excludedNamespaces: ["kube-*", "my-namespace"]
      processes: ["*"]
    - excludedNamespaces: ["audit-excluded-ns"]
      processes: ["audit"]
    - excludedNamespaces: ["mutation-excluded-ns"]
      processes: ["mutation-webhook"]
```

Processes: `audit` (omit from audit results), `webhook` (omit from the admission webhook), `sync` (do not sync into OPA), `mutation-webhook`, and `*` for all current and future processes. To exclude namespaces for a single constraint, use `excludedNamespaces` in that constraint match instead.

Because Gatekeeper itself evaluates these exemptions, the API server still calls the webhook for those namespaces, so a Gatekeeper outage can still affect them.

The Config resource is alpha. Keep in mind it applies to all constraints at once, so it is the right place for platform namespaces such as `kube-*`, whereas a per-constraint `excludedNamespaces` list is the right place for an exemption that belongs to one policy only. A `sync` exclusion also stops those namespaces being replicated into OPA for referential constraints.

## Checked

2026-11-08. Confirmed against exempt-namespaces.md (Config resource section; read in full): alpha state, name must be config, wildcard matching, processes list, per-constraint excludedNamespaces, difference between config exclusion and the webhook flag (webhook still called). Removed or corrected: the claim that the Config must live in gatekeeper-system is now stated as the example's placement; removed the claim that per-constraint excludedNamespaces share the same wildcard syntax (not stated in this page).

Method: documentation only; no commands were run.
