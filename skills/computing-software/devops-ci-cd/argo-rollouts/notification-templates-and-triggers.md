---
id: computing-software.devops-ci-cd.argo-rollouts.notification-templates-and-triggers
name: notification-templates-and-triggers
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [notifications, templates, custom-triggers, golang-template, notifications-engine, argo-rollouts]
level: advanced
status: docs-checked
description: "Write notification templates in Go html/template and understand the fields every template can read."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/notifications/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A notification template is a stateless function that generates message content using Go's `html/template`. It is reusable across triggers and lives in `argo-rollouts-notification-configmap` under a `template.<name>` key.

```yaml
data:
  template.my-purple-template: |
    message: |
      Rollout {{.rollout.metadata.name}} has purple image
    slack:
      attachments: |
        [{
          "title": "{{ .rollout.metadata.name}}",
          "color": "#800080"
        }]
```

Every template can read:

- `rollout`: the Rollout object.
- `recipient`: the recipient name.
- `context`: user-defined context from the notifications ConfigMap.

The `message` field gives a basic notification for any service. Service-specific fields enable richer output: blocks and attachments for Slack, a subject for email, a URL path and body for webhooks. Each service's page under the notification services documentation lists them.

Administrators can also add custom triggers that choose when to send and which template to use, in the same ConfigMap. A trigger has a name, a `when` condition expression and the templates to `send`.

Verify delivery in the target channel.

## Checked
2026-11-08. Confirmed against the Argo Rollouts Notifications page: `argo-rollouts-notification-configmap`, `template.<name>` keys, Go html/template, the `rollout`, `recipient` and `context` fields, service-specific fields, and custom triggers. Removed the uncited list of services, the narrow-trigger advice and the `kubectl argo rollouts notifications` CLI commands, none of which are on that page.
Method: documentation only; no commands were run.
