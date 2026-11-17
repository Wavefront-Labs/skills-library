---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-custom-resource-targets
name: external-secrets-operator-custom-resource-targets
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [manifest-target, configmap, generic-targets, alpha]
level: sme
status: docs-checked
description: "Populate ConfigMaps and custom resources from ExternalSecrets with the alpha manifest target, its enabling flag, RBAC and path targeting."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/targeting-custom-resources.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Heavy alpha at the time of writing. ESO can manage resources other than Secrets, such as ConfigMaps or CRDs, but custom resources are not encrypted at rest, so use it only for non-sensitive data or resources protected another way.

Requirements:
- Start the controller with `--unsafe-allow-generic-targets`.
- Grant RBAC through the chart: `genericTargets.enabled: true` with `resources` listing `apiGroups`, `resources` and `verbs`.
- Only namespaced resources, in the same namespace as the ExternalSecret.
- About 20 percent slower than Secrets.

Templates work as usual. For nested resources use `target` with a dot path such as `spec.database`, or array notation like `spec.rules[0].from[0].source.notRemoteIpBlocks`; intermediate maps and arrays are created and siblings preserved, and a path cannot start with a bare index. When unset, `target` defaults to `Data`. When templating `data` entries, set `property` (the value is not an object in scope).

Drift is corrected immediately via informers, and ESO adds the label `externalsecrets.external-secrets.io/managed: "true"`.

## Checked

2026-11-03. Claims were read against guides/targeting-custom-resources.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
