---
id: computing-software.devops-ci-cd.argo-cd.health-checks-for-crds-and-operators
name: health-checks-for-crds-and-operators
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, crd-health, custom-health-check, lua-health-check]
level: advanced
status: docs-checked
description: "Give CRDs (cert-manager, ExternalSecret, Crossplane, operators) meaningful Argo CD health: built-in resource_customizations, writing Lua for status conditions, sync wave ordering."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/health/", "https://github.com/argoproj/argo-cd/tree/master/resource_customizations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Health for CRDs and operator resources

Argo CD relies on the status fields CRD authors define, so it can only judge a custom resource reliably when a health check exists for it. Bundled Lua checks live in the `resource_customizations` directory of the argo-cd repository (`<group>/<kind>/health.lua`); look there for your version before writing one.

## Generic condition-based check (argocd-cm)
```yaml
data:
  resource.customizations.health.example.com_Database: |
    hs = { status = "Progressing", message = "Waiting for status" }
    if obj.status ~= nil and obj.status.conditions ~= nil then
      for _, c in ipairs(obj.status.conditions) do
        if c.type == "Ready" and c.status == "True" then
          return { status = "Healthy", message = c.message or "Ready" }
        end
        if c.type == "Ready" and c.status == "False" and c.reason == "Failed" then
          return { status = "Degraded", message = c.message }
        end
      end
    end
    return hs
```
Key format: `<group>_<kind>` (`resource.customizations.health.cert-manager.io_Certificate`).
Wildcard keys exist only in some key forms (the health page shows a quoted `resource.customizations` entry for `"*.aws.crossplane.io/*"`); read that section before using one.

## Observed generation
Guard against stale status: return Progressing when
`obj.status.observedGeneration ~= obj.metadata.generation`.

## Ordering with waves
Put the CR in a later wave than the CRD and operator; with a health check, wave N+1 waits for the CR
to become Healthy.

## Verify
- [ ] App tree shows the CR as Progressing until the operator reports Ready, then Healthy.

## Checked
2026-10-28. Confirmed on the Argo CD health page: Argo CD relies on CRD-defined status fields and needs custom health checks for CRDs without a built-in one; bundled scripts are in the `resource_customizations` directory of the argo-cd repository; key format `resource.customizations.health.<group_kind>`; `observedGeneration` guidance; wildcards only in some forms with a quoted GVK key. Confirmed on the sync waves page: later waves wait for earlier waves to be healthy.
Removed (not confirmed): "no health check is always Healthy", the list of bundled CRDs, the `resource.customizations.health.*.crossplane.io_*` wildcard form, and the `SkipDryRunOnMissingResource=true` advice.

Method: documentation only; no commands were run.
