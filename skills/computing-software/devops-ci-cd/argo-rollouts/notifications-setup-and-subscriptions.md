---
id: computing-software.devops-ci-cd.argo-rollouts.notifications-setup-and-subscriptions
name: notifications-setup-and-subscriptions
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [notifications, subscription, slack, argo-rollouts-notification-configmap, triggers, annotations, argo-rollouts]
level: practitioner
status: docs-checked
description: "Configure the notification ConfigMap, a service such as Slack, and subscribe Rollouts through annotations."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/notifications/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Notifications (since v1.1) use the Notifications Engine. Administrators configure triggers, templates and services in the `argo-rollouts-notification-configmap` ConfigMap; end users subscribe by annotating Rollouts.

Quick start: apply the pre-configured templates from `notifications-install.yaml` alongside `install.yaml` (a Kustomization can list both release URLs as resources). Then add a service, for example Slack:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argo-rollouts-notification-configmap
data:
  service.slack: |
    token: $slack-token
---
apiVersion: v1
kind: Secret
metadata:
  name: argo-rollouts-notification-secret
stringData:
  slack-token: <my-slack-token>
```

Built-in triggers: `on-analysis-run-error`, `on-analysis-run-failed`, `on-analysis-run-running`, `on-rollout-aborted`, `on-rollout-completed`, `on-rollout-paused`, `on-rollout-step-completed`, `on-rollout-updated`, `on-scaling-replica-set`.

Subscribe with `notifications.argoproj.io/subscribe.<trigger>.<service>: <recipient>`; recipients are separated by semicolons:

```yaml
metadata:
  annotations:
    notifications.argoproj.io/subscribe.on-rollout-step-completed.slack: my-channel1;my-channel2
```

Namespace-based configuration (since v1.6): create the same ConfigMap (and secret) in the Rollout's namespace and start the controller with `--self-service-notification-enabled`; both configs are then used.

As in the docs example, the token lives in the Secret (`slack-token`) and the ConfigMap references it as `$slack-token` instead of inlining it. Verify by changing a Rollout and confirming the message arrives; the plugin also has a `kubectl argo rollouts notifications` command group for managing notification settings.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/notifications/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts/.

Removed or corrected: the RBAC advice and the notifications template notify command (not on the pages).

Method: documentation only; no commands were run.
