---
id: computing-software.devops-ci-cd.flux.alert-and-provider-basics
name: alert-and-provider-basics
category: computing-software
field: devops-ci-cd
product: flux
tags: [alert, provider, notification-controller, slack, eventsources]
level: sme
status: docs-checked
description: "Send Flux events to Slack and other systems with a Provider and an Alert referencing event sources."
sources:
  - https://fluxcd.io/flux/components/notification/alerts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Provider says where to send (type, address, channel, credentials); an Alert says which events to send. The Alert references a Provider in its own namespace; the current page uses API `notification.toolkit.fluxcd.io/v1`.

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1
kind: Provider
metadata:
  name: slack-bot
  namespace: flux-system
spec:
  type: slack
  channel: general
  address: https://slack.com/api/chat.postMessage
  secretRef:
    name: slack-bot-token
---
apiVersion: notification.toolkit.fluxcd.io/v1
kind: Alert
metadata:
  name: slack
  namespace: flux-system
spec:
  providerRef:
    name: slack-bot
  eventSeverity: error
  eventMetadata:
    cluster: my-cluster
  eventSources:
    - kind: GitRepository
      name: '*'
    - kind: Kustomization
      name: '*'
```

The Slack example needs a Secret first: `kubectl -n flux-system create secret generic slack-bot-token --from-literal=token=xoxb-YOUR-TOKEN`. Provider options beyond this example are on the Providers page (not read for this skill).

`.spec.providerRef.name` and `.spec.eventSources` are required. Each `eventSources` item needs `kind`, `name` (or the `*` wildcard) and optionally `namespace`, which defaults to the Alert namespace. `eventMetadata` adds fixed key-value context to dispatched events. `.spec.suspend: true` stops event processing. With `--no-cross-namespace-refs=true` on the controller, alerts can only reference sources in their own namespace.

## Checked

2026-11-08. Read in full: https://github.com/fluxcd/notification-controller/blob/main/docs/spec/v1/alerts.md.

Removed or corrected: the v1beta3 API version (the current page uses v1), the Provider type list, proxySecretRef and certSecretRef, and the verification advice, none of which is on the Alerts page.

Method: documentation only; no commands were run.
