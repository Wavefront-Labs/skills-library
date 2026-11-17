---
id: computing-software.devops-ci-cd.argo-cd.testing-custom-lua-health-checks
name: testing-custom-lua-health-checks
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, lua-health-testing, custom-health-check, health-lua, resource-overrides-cli]
level: advanced
status: docs-checked
description: "Write and test custom Lua health checks for CRDs in Argo CD: argocd-cm keys, hs.status/message, local testing with argocd admin settings resource-overrides, and upstream tests."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/health/#custom-health-checks", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_admin_settings_resource-overrides_health/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Lua health checks and how to test them

## 1. Write
```yaml
# argocd-cm
data:
  resource.customizations.health.db.example.com_PostgresCluster: |
    hs = {}
    if obj.status ~= nil and obj.status.conditions ~= nil then
      for _, c in ipairs(obj.status.conditions) do
        if c.type == "Ready" and c.status == "True" then
          hs.status = "Healthy"; hs.message = c.message or "ready"; return hs
        end
        if c.type == "Ready" and c.status == "False" and c.reason == "Failed" then
          hs.status = "Degraded"; hs.message = c.message; return hs
        end
      end
    end
    hs.status = "Progressing"
    hs.message = "Waiting for Ready condition"
    return hs
```
Key: `resource.customizations.health.<group>_<Kind>` in `argocd-cm`; the script sets `hs.status` and `hs.message` and returns `hs`. Where the CRD uses `observedGeneration` correctly in its status, the docs describe using it so a stale condition is not read as healthy.

## 2. Test locally against real objects
```bash
kubectl get postgrescluster main -n db -o yaml > pg.yaml
argocd admin settings resource-overrides health pg.yaml --argocd-cm-path ./argocd-cm.yaml
```
Keep fixture YAMLs for each state (ready, failed, initialising) and run the command in CI on
changes to `argocd-cm.yaml`.

## 3. Contribute upstream
The docs show the layout per resource kind: `health.lua`, `health_test.yaml` (test inputs and expected results) and a `testdata` directory with test resource YAMLs; see the Custom Health Checks page for the exact path and how the tests are run.

## Gotchas
- Standard Lua libraries are disabled by default for health checks; enable them per resource with `resource.customizations.useOpenLibs.<group>_<kind>`.

## Verify
- [ ] The admin command returns the expected status for every fixture; the live app shows the CR's real readiness.

## Checked
2026-10-28. Confirmed on the Argo CD health page and the `argocd admin settings resource-overrides health` reference: key format `resource.customizations.health.<group_kind>`, `hs.status` / `hs.message`, the `observedGeneration` guidance, `useOpenLibs`, the `health.lua` / `health_test.yaml` / `testdata` layout, and `argocd admin settings resource-overrides health ./deploy.yaml --argocd-cm-path ./argocd-cm.yaml`.
Removed (not confirmed): the list of allowed status values, the Lua-error-gives-Unknown statement, the `go test` command, the wildcard key note, and the sample output line.

Method: documentation only; no commands were run.
