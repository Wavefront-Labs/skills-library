---
id: computing-software.cloud-infrastructure-engineering.kubernetes.argocd-notifications-and-custom-health-checks
name: argocd-notifications-and-custom-health-checks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, argocd, argocd-notifications, custom-health-check, lua, gitops, alerting]
level: advanced
status: docs-checked
description: "Notify teams on Argo CD sync and health events via triggers, templates and subscriptions, and write Lua health checks so CRDs report real Healthy/Degraded status."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/catalog/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/health/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo CD notifications and custom health checks

## Notifications
Built into Argo CD (argocd-notifications-controller). Config in `argocd-notifications-cm`,
secrets in `argocd-notifications-secret`. Install the trigger/template catalog
(`kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/notifications_catalog/install.yaml`),
then add a service:
```yaml
# argocd-notifications-cm
data:
  service.slack: |
    token: $slack-token
  context: |
    argocdUrl: https://argocd.example.com
  trigger.on-sync-failed: |
    - when: app.status.operationState.phase in ['Error', 'Failed']
      send: [app-sync-failed]
  trigger.on-health-degraded: |
    - when: app.status.health.status == 'Degraded'
      oncePer: app.status.sync.revision
      send: [app-health-degraded]
  template.app-sync-failed: |
    message: |
      {{.app.metadata.name}} sync failed at {{.app.status.operationState.finishedAt}}:
      {{.app.status.operationState.message}}
      {{.context.argocdUrl}}/applications/{{.app.metadata.name}}
```
Subscribe with annotations on the Application or AppProject (project-level covers all its apps):
```yaml
metadata:
  annotations:
    notifications.argoproj.io/subscribe.on-sync-failed.slack: payments-deploys
    notifications.argoproj.io/subscribe.on-health-degraded.slack: payments-alerts
```
`oncePer` sends only when the named field value changes; with one repo feeding many apps the
docs prefer `app.status?.operationState.syncResult.revision`. Services include Slack, email,
webhook, Teams, PagerDuty, GitHub, Opsgenie and Mattermost. Debug:
```bash
argocd admin notifications trigger run on-sync-failed api -n argocd
argocd admin notifications template notify app-sync-failed api --recipient slack:test -n argocd
```

## Custom health checks
For a CRD with no built-in check, add Lua in `argocd-cm`, key
`resource.customizations.health.<group>_<kind>` (core kinds omit the group prefix). The docs
use `cert-manager.io/Certificate` as the example:
```yaml
data:
  resource.customizations.health.cert-manager.io_Certificate: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.conditions ~= nil then
        for i, condition in ipairs(obj.status.conditions) do
          if condition.type == "Ready" and condition.status == "False" then
            hs.status = "Degraded"
            hs.message = condition.message
            return hs
          end
          if condition.type == "Ready" and condition.status == "True" then
            hs.status = "Healthy"
            hs.message = condition.message
            return hs
          end
        end
      end
    end
    hs.status = "Progressing"
    hs.message = "Waiting for certificate"
    return hs
```
Statuses: `Healthy`, `Progressing`, `Degraded`, `Suspended`, `Missing`, `Unknown`.
Always handle `obj.status == nil` (fresh objects). Many common CRDs already ship health
checks in Argo CD (the repo `resource_customizations` directory); check before writing one. To
share one check across kinds, the docs show a wildcard in the kind or group under the
`resource.customizations` key (for example `ec2.aws.crossplane.io/*`).

## Test health Lua offline
```bash
argocd admin settings resource-overrides health ./cluster.yaml --argocd-cm-path ./argocd-cm.yaml
```

## Verify
- [ ] Breaking a CR turns the app Degraded and a Slack message arrives once, with a link.

## Checked

Documentation release: Argo CD stable docs (argo-cd repo docs/, latest release v3.5.6, repo commit 2026-10-25).
Confirmed: catalog install command; `argocd-notifications-cm` and `argocd-notifications-secret`; trigger `when`/`send`/`oncePer`; subscription annotation `notifications.argoproj.io/subscribe.<trigger>.<service>` on Applications and AppProjects; the `argocd admin notifications trigger run` and `template notify` commands (with `-n`); `resource.customizations.health.<group>_<kind>`, the six health statuses, wildcard form under `resource.customizations`, and `argocd admin settings resource-overrides health RESOURCE_YAML --argocd-cm-path`.
Replaced: the CloudNativePG example (its phase strings are not in Argo CD docs) with the documented cert-manager example; corrected the wildcard claim, which applies to `resource.customizations`, not the per-kind key.

Method: documentation only; no commands were run.
