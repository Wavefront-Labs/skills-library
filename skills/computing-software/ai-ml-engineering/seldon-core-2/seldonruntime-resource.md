---
id: computing-software.ai-ml-engineering.seldon-core-2.seldonruntime-resource
name: seldonruntime-resource
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, seldonruntime, crd, overrides, disableautoupdate, namespace-install]
level: practitioner
status: docs-checked
description: "Create a SeldonRuntime to install Seldon Core 2 components in a namespace from a SeldonConfig, with per-component overrides, and control update propagation."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/seldonruntime.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SeldonRuntime resource

A SeldonRuntime creates an instance of Seldon in one namespace, based on a named SeldonConfig.

## Minimal use
```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: SeldonRuntime
metadata:
  name: seldon
  namespace: seldon-mesh
spec:
  seldonConfig: default
```

## Spec fields
- `seldonConfig`: the base configuration.
- `overrides`: list of `name`, `disable`, `replicas`, `serviceType`, `podSpec`.
- `config`: the SeldonConfiguration block, same as in SeldonConfig.
- `disableAutoUpdate`: stop immediate reconciliation when the referenced SeldonConfig changes.

## Overriding a component
To override a PodSpec, give the component name in `overrides` and the container name in the PodSpec. This lowers hodometer limits while the rest comes from `default`:

```yaml
spec:
  overrides:
  - name: hodometer
    podSpec:
      containers:
      - name: hodometer
        resources:
          limits:
            memory: 64Mi
            cpu: 20m
  seldonConfig: default
```

## Update propagation
When a SeldonConfig changes, every SeldonRuntime that references it is updated immediately. Set `spec.disableAutoUpdate` to avoid that; the runtime then updates only when you change the SeldonRuntime itself.

The helm chart `seldon-core-v2-runtime` creates this resource plus default Servers.

## Checked

Confirmed against the Seldon Runtime page: the minimal manifest, spec fields seldonConfig, overrides (name, disable, replicas, serviceType, podSpec), config and disableAutoUpdate, the hodometer override example, update propagation, and the seldon-core-v2-runtime Helm chart.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb kubernetes/resources/seldonruntime.md page (raw markdown).
