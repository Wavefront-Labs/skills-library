---
id: computing-software.cloud-infrastructure-engineering.garage.kubernetes-discovery-section
name: kubernetes-discovery-section
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [kubernetes-discovery, garagenodes-crd, skip-crd, namespace]
level: advanced
status: docs-checked
description: "Configure [kubernetes_discovery] so Garage finds peers through custom resources."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage can discover cluster members through Kubernetes custom resources. A `[kubernetes_discovery]` section must exist and contain at least `namespace` and `service_name`.

- `namespace`: the namespace in which the custom resources are configured.
- `service_name`: added as a label on the advertised resources to filter them, which allows several deployments to share one namespace.
- `skip_crd`: when `true`, Garage does not automatically create and patch the `garagenodes.deuxfleurs.fr` custom resource definition. You must then create the CRD yourself.

By default Garage creates and patches the CRD itself; setting `skip_crd = true` disables that, and you install the CRD ahead of time.

The full example on the page shows `skip_crd = false`.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed the required namespace and service_name, the label purpose of service_name and the skip_crd behaviour with the CRD name. Removed the paragraphs on rpc settings, a Kubernetes cookbook page and bootstrap_peers, which the page does not state for this section.
Method: documentation only; no commands were run.
