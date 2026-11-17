---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventbus-nats-streaming-deprecated
name: argo-events-eventbus-nats-streaming-deprecated
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, nats-streaming, stan, deprecated, native, exotic, token-auth, migration]
level: practitioner
status: docs-checked
description: "Maintain existing NATS Streaming EventBuses (native or exotic) and their limits, and plan the move to JetStream."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventbus/stan.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventbus nats streaming deprecated

NATS Streaming (STAN) reached end of life in June 2023, and prometheus-nats-exporter dropped STAN support. Existing STAN EventBuses keep working, but new ones should use JetStream.

Native bus (`spec.nats.native`) creates a StatefulSet, 3 replicas by default and minimum (NATS recommends 3 to 5, odd numbers). Settings: `auth` (`none` default, or `token`, in which case a token is generated into Secrets for client and server and EventSource and Sensor pods load the client secret automatically), `persistence` (storageClassName, accessMode, volumeSize), `nodeSelector`, `tolerations`, `affinity`, `securityContext`, `priority`, `priorityClassName`, `serviceAccountName`, `imagePullSecrets`. `antiAffinity` is deprecated in v1.3 and removed in v1.5; use `affinity`.

Limits: `maxAge` default 72h; `maxMsgs` 1,000,000 per channel, `maxBytes` 1GB, `maxSubs` 1000 and `maxPayload` 1MB are defaults where 0 means unlimited.

Exotic bus (`spec.nats.exotic`) connects to your existing service with `url`, `clusterID`, `auth: token` and an `accessSecret` (name and key). All events in a namespace go to one channel named `eventbus-{namespace}`.

Check the resolved config with `kubectl get eventbus default -o json | jq '.status.config'`.

## Checked

2026-11-04. Confirmed against the NATS Streaming EventBus page: deprecation note, native defaults (3 replicas, minimum 3, `auth` none or token with generated Secrets), the property list, `antiAffinity` deprecation (v1.3, removal v1.5), limit defaults, the exotic example, the status config command and the `eventbus-{namespace}` channel. Reworded the limits sentence because the page states 0 means unlimited only for the four count and size limits, not `maxAge`.
Method: documentation only; no commands were run.
