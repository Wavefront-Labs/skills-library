---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-dashboard-customize-links
name: kubeflow-dashboard-customize-links
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [customize-dashboard, centraldashboard-config, menu-links, external-links, virtualservice]
level: practitioner
status: docs-checked
description: "Customize the Central Dashboard menu through the centraldashboard-config ConfigMap: externalLinks, menuLinks, documentationItems and exposing an in-cluster app via VirtualService."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/central-dash/customize.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dashboard customize links

The dashboard reads a ConfigMap named by `CD_CONFIGMAP_NAME` on the central-dashboard Deployment (default `centraldashboard-config`). Its `links` key holds JSON with `menuLinks`, `externalLinks`, `quickLinks` and `documentationItems`.

- **externalLinks** (sidebar, sites outside the cluster): objects with `type: "item"`, `iframe: false`, `text`, `link`, `icon`.
- **documentationItems** (Documentation section of Home): `text`, `desc`, `link`.
- **menuLinks** (sidebar, in-cluster apps): `type: "item"`, `link` (path), `text`, `icon`.

Icons are iron-icon names without the `icons:` prefix (for `icons:launch` use `launch`; for other sets, use `social:mood`).

To expose a non-Kubeflow in-cluster app: it needs an Istio sidecar and a Kubernetes Service, plus a VirtualService on gateway `kubeflow/kubeflow-gateway` that matches prefix `/my-app/`, adds header `x-forwarded-prefix: /my-app`, rewrites the URI to `/` and routes to the Service. The app then appears under `/_/my-app/` on the gateway; set the menu link to `/my-app/`.

For per-profile app instances use `{ns}` in the link, such as `/my-app/{ns}/`, and expose each under `/my-app/<namespace>/`; existing AuthorizationPolicies then restrict access to profile contributors.

Every request carries a `kubeflow-userid` header with the user email. To prevent spoofing, only allow traffic from the gateway ServiceAccount (an ALLOW AuthorizationPolicy) and require `ISTIO_MUTUAL` TLS through a DestinationRule.

## Checked

Confirmed the ConfigMap name and CD_CONFIGMAP_NAME variable, the externalLinks, documentationItems and menuLinks fields, the icon naming rule, the VirtualService settings, the {ns} pattern and the kubeflow-userid header guidance. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website central-dash customize.md page, read in full.
