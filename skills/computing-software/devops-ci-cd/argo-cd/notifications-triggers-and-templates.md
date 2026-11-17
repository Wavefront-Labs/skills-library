---
id: computing-software.devops-ci-cd.argo-cd.notifications-triggers-and-templates
name: notifications-triggers-and-templates
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, argocd-notifications, notifications-controller, notification-triggers, notification-templates, argocd-notifications-cm, argocd-notifications-secret, subscriptions, notified-annotation, slack-service, teams-service, email-service, webhook-service, github-service, grafana-service, pagerduty-service, oncesync, on-sync-succeeded, on-health-degraded, on-deployed, default-subscriptions, commit-status-webhook, notification-catalog, gitops, kubernetes]
level: practitioner
status: gated
description: "Tell people and systems what Argo CD did: notification services, triggers with oncePer, Go templates, app and project subscriptions, commit status, debugging."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/triggers/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/templates/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/catalog/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Notifications: triggers and templates

**Goal:** a deploy to production posts once to the team channel with the commit, author
and diff link; a degraded app pages; GitHub shows a commit status — and nothing repeats
every reconcile loop.

## 1. Pieces
The `argocd-notifications-controller` watches Applications; `argocd-notifications-cm`
defines **services** (where), **triggers** (when), **templates** (what); annotations on
Applications/AppProjects **subscribe**. Secrets (tokens) live in `argocd-notifications-secret`.
Install the **catalog** (see the notifications catalog page for the install manifest) for ready-made `on-deployed`,
`on-sync-failed`, `on-health-degraded`, `on-sync-running`, `on-sync-status-unknown`,
`on-created`, `on-deleted` and matching templates.

## 2. Services
The per-service settings below (Slack, webhook, Teams, email, PagerDuty keys and scopes) come from the service pages, which were not read (gated: unconfirmed, source is paywalled or blocked); confirm each against the Argo CD notifications services docs.
```yaml
# argocd-notifications-cm
data:
  service.slack: |
    token: $slack-token                       # key in argocd-notifications-secret
    # apiURL / disableUnfurl / icon available
  service.webhook.github-status: |
    url: https://api.github.com
    headers:
      - { name: Authorization, value: token $github-token }
  service.teams: |
    recipientUrls:
      team-a: $teams-team-a-webhook
  service.email.smtp: |
    host: smtp.example.com
    port: 587
    username: $email-username
    password: $email-password
    from: argocd@example.com
  service.pagerduty: |
    serviceKeys: { prod: $pagerduty-prod-key }
```

## 3. Triggers
```yaml
  trigger.on-deployed: |
    - description: Application is synced and healthy. Triggered once per commit.
      oncePer: app.status.operationState?.syncResult?.revision
      send: [app-deployed]
      when: app.status.operationState != nil and app.status.operationState.phase in ['Succeeded'] and app.status.health.status == 'Healthy'
  trigger.on-health-degraded: |
    - send: [app-health-degraded]
      when: app.status.health.status == 'Degraded'
  trigger.on-sync-failed: |
    - send: [app-sync-failed]
      when: app.status.operationState != nil and app.status.operationState.phase in ['Error', 'Failed']
  trigger.on-sync-status-unknown: |
    - send: [app-sync-status-unknown]
      when: app.status.sync.status == 'Unknown'
      oncePer: app.status.sync.revision
```
`when` is an [expr](https://github.com/expr-lang/expr) expression over `app`, `time`,
`repo`, `sync`. **`oncePer`** is what stops the "every 3 minutes" spam: the controller
records the value it already notified for (the controller stores this on the app; annotation name gated: unconfirmed, source is paywalled or blocked). The docs use `oncePer: app.status.sync.revision` to notify once per commit and, for mono repos, suggest a custom annotation such as `app.metadata.annotations["example.com/version"]`.

## 4. Templates
```yaml
  template.app-deployed: |
    message: |
      {{if eq .serviceType "slack"}}:white_check_mark:{{end}} {{.app.metadata.name}} deployed to {{.app.spec.destination.namespace}}
    slack:
      attachments: |
        [{
          "title": "{{ .app.metadata.name }}",
          "title_link": "{{.context.argocdUrl}}/applications/{{.app.metadata.name}}",
          "color": "#18be52",
          "fields": [
            {"title": "Revision", "value": "{{ trunc 7 .app.status.sync.revision }}", "short": true},
            {"title": "Author",   "value": "{{ (call .repo.GetCommitMetadata .app.status.sync.revision).Author }}", "short": true},
            {"title": "Message",  "value": "{{ (call .repo.GetCommitMetadata .app.status.sync.revision).Message | trunc 120 }}", "short": false}
          ]
        }]
    teams: { title: "Deployed", text: "{{.app.metadata.name}} → {{.app.spec.destination.namespace}}" }
  template.github-commit-status: |
    webhook:
      github-status:
        method: POST
        path: /repos/{{call .repo.FullNameByRepoURL .app.spec.source.repoURL}}/statuses/{{.app.status.operationState.operation.sync.revision}}
        body: |
          {"state": "{{if eq .app.status.operationState.phase "Succeeded"}}success{{else}}failure{{end}}",
           "description": "ArgoCD", "target_url": "{{.context.argocdUrl}}/applications/{{.app.metadata.name}}", "context": "continuous-delivery/{{.app.metadata.name}}"}
```
Templates use Go's `html/template` package per the docs; `.context.argocdUrl` from `context: | argocdUrl: https://…`
in the ConfigMap. `.repo.GetCommitMetadata` needs repo credentials the notifications
controller can read (same `argocd` namespace Secrets). Email templates support `subject`
and HTML `body`.

## 5. Subscriptions
Per app (annotation):
```yaml
metadata:
  annotations:
    notifications.argoproj.io/subscribe.on-deployed.slack: team-a-deploys        # channel name without #
    notifications.argoproj.io/subscribe.on-health-degraded.pagerduty: prod
    notifications.argoproj.io/subscribe.on-sync-failed.teams: team-a
```
Per project: same annotations on the AppProject (applies to all its apps). Instance-wide:
```yaml
  subscriptions: |
    - recipients: [slack:platform-alerts, webhook:github-status]
      triggers: [on-sync-failed, on-deployed]
      selector: env=prod                      # label selector on Applications
```
Multiple recipients: `team-a;team-b`. ApplicationSet templates can carry the annotations
so generated apps are subscribed automatically.

## 6. Debugging
```bash
argocd admin notifications template notify app-deployed web --recipient slack:test-channel   # (gated: unconfirmed, source is paywalled or blocked)
argocd admin notifications trigger get on-deployed                                            # trigger state per app
argocd admin notifications trigger run on-deployed web                                        # evaluate conditions
kubectl -n argocd logs deploy/argocd-notifications-controller | grep -i web
```
Nothing sent: check whether the trigger already notified for that `oncePer` value, the subscription annotation spelling, and that the secret key names match `$name`.

## Verify
- [ ] A sync to a subscribed app posts once to Slack with revision + author; a re-sync of the same revision posts nothing.
- [ ] `Degraded` triggers PagerDuty; recovery is visible via `on-deployed`.
- [ ] GitHub shows a `continuous-delivery/<app>` status on the deployed commit.
- [ ] `trigger run` output explains why a trigger did or did not fire.

## Checked

2026-11-02. Confirmed against the Argo CD notifications overview, triggers, templates and catalog pages: argocd-notifications-cm and argocd-notifications-secret, subscribe annotations on Application/AppProject (notifications.argoproj.io/subscribe.<trigger>.<service>), trigger structure with when/oncePer/send, expr-based conditions, catalog trigger names, templates use html/template. Fixed: Go text/template + sprig (docs say html/template). Removed: Helm notifications.cm install route, Slack scope detail, Slack 429 rate-limit claim, multi-condition ordering claim. Gated: the notified annotation name, service configuration keys and the admin notifications --recipient flag.

Method: documentation only; no commands were run.
