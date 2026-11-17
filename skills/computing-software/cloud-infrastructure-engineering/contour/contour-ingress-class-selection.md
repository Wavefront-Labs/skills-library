---
id: computing-software.cloud-infrastructure-engineering.contour.contour-ingress-class-selection
name: contour-ingress-class-selection
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [ingress-class, ingressclassname, ingress-class-name-flag, annotation-precedence, multiple-contour-instances]
level: practitioner
status: docs-checked
description: "How Contour selects Ingress and HTTPProxy objects by class: annotations vs spec.ingressClassName, --ingress-class-name list, defaults and precedence."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/annotations.md", "https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/ingress.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ingress class selection

Applies to Ingress and HTTPProxy. The class can be given by annotation (`kubernetes.io/ingress.class` or `projectcontour.io/ingress.class`) or by `spec.ingressClassName` (preferred). If both are set, the annotation takes precedence.

Default behaviour (no `--ingress-class-name`):
- Contour accepts objects with class `contour` or with no class at all.
- Any other class value: ignored.

With `contour serve --ingress-class-name=<name>` (a comma-separated list is allowed):
- No class set: Contour ignores the object.
- Class not matching any listed name: ignored.
- Class matching: served.

```yaml
spec:
  ingressClassName: contour-internal
```

Notes:
- Contour does not require an IngressClass resource with that name to exist; the name is just a filter identifier.
- The IngressClass flag is the tool for migrating from another controller or running multiple Contour instances (for example public and internal), each with its own class and Envoy service.
- `ingress-status-address` (or the Envoy Service named by `--envoy-service-name` and `--envoy-service-namespace`) provides the status address written to Ingress objects.
- Without the flag, an Ingress with no class is served by Contour as well as by any other controller that accepts unclassed Ingresses, so set a class when running several controllers.

## Checked

2026-11-08: read the Contour docs config/annotations (Ingress Class) and config/ingress (IngressClass and Status). Confirmed: both annotation names, spec.ingressClassName preferred, annotation precedence, default class contour or none, flag behaviour with comma-separated list, no IngressClass resource required, and the status address flags.

Method: documentation only; no commands were run.
