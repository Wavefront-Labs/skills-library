---
id: computing-software.cloud-infrastructure-engineering.crossplane.connection-details-secret
name: connection-details-secret
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [connection-details, secret, xr, v2, composition]
level: advanced
status: docs-checked
description: "Expose XR connection details in v2 by composing a Secret from composed resources' secrets."
sources:
  - https://docs.crossplane.io/latest/guides/connection-details-composition/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Crossplane v2 removed automatic connection details for XRs only. Managed resources still support `writeConnectionSecretToRef`. To expose details, include a Kubernetes `Secret` in the Composition that aggregates them.

Pattern:

1. Each composed resource writes its connection details to its own Secret via `writeConnectionSecretToRef`.
2. The composition reads those (observed) and composes a `Secret` resource holding the combined keys, for example `user-0`, `password-0`, `user-1`, `password-1`.
3. The XR exposes the Secret, named from the XR's `spec.writeConnectionSecretToRef.name`.

The XRD schema must define `.spec.writeConnectionSecretToRef.name`. For a Cluster-scoped XRD also add `.namespace`, so users can say where the Secret goes.

Which function to use:

- function-patch-and-transform aggregates automatically: set `connectionDetails` on each composed resource and a `writeConnectionSecretToRef` section in the function input.
- function-pythonic also aggregates automatically: assign `self.connection[key] = resource.connection[key]`.
- function-go-templating, function-python and function-kcl read observed connection details and compose the Secret by hand. Go templating and KCL give details already base64-encoded; function-python gives plaintext bytes to decode and put in `stringData`.
- The guide also uses function-auto-ready to mark composed resources ready.

The same pattern covers database credentials, cluster certificates and endpoints from services.

A Cluster-scoped XR composing a Secret must set its namespace explicitly, or it fails with `an empty namespace may not be set when a resource name is provided`. Handle the first reconcile, when observed resources do not exist yet.

## Checked

Pattern, XRD field, function behaviours, encoding differences and the empty-namespace error confirmed on the Connection Details Composition guide. The skill wrongly listed function-pythonic as manual-only and carried an unsourced naming-advice sentence; both fixed.

Method: docs-checked 2026-11-09 against the raw Connection Details Composition guide (docs repo, current content folder), read in full.
