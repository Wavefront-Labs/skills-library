---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventbus-jetstream-managed
name: argo-events-eventbus-jetstream-managed
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, jetstream, eventbus, replicas, persistence, streamconfig, nats, statefulset]
level: practitioner
status: docs-checked
description: "Configure a managed JetStream EventBus with version, replicas, persistence, streamConfig and settings, and know its TLS and stream layout."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventbus/jetstream.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventbus jetstream managed

JetStream is the NATS community streaming server that replaces NATS Streaming, which reached end of life in June 2023. The simplest EventBus (`spec.jetstream.version: latest`) brings up a 3-replica StatefulSet, but never use `latest` in real deployments; pin a version. Versions supported are managed in the controller ConfigMap (`kubectl get configmap argo-events-controller-config -o yaml`), which can be updated to add more.

A fuller spec:

```yaml
spec:
  jetstream:
    version: latest
    replicas: 5
    persistence:
      storageClassName: standard
      accessMode: ReadWriteOnce
      volumeSize: 10Gi
    streamConfig: |
      maxAge: 24h
    settings: |
      max_file_store: 1GB
    startArgs:
      - "-D"
```

`streamConfig` and `settings` default to values in `argo-events-controller-config`; `startArgs` such as `-D` enable debug logs.

Security: TLS is on for all client-server traffic and between nodes, with password authentication by default.

Under the hood there is one Stream called `default` with one set of settings and many subjects, each named `default.<eventsourcename>.<eventname>`. Sensors subscribe to the subjects they need using durable consumers.

## Checked

2026-11-04. Confirmed against the EventBus Jetstream page: end of life of NATS Streaming in June 2023, the `latest` example and the 3-replica StatefulSet, the warning not to use `latest`, the controller ConfigMap command, the `replicas`/`persistence`/`streamConfig`/`settings`/`startArgs` example, the TLS and password security paragraph, and the `default` stream with `default.<eventsourcename>.<eventname>` subjects and durable consumers. Removed a conclusion about message retention that the page does not state.
Method: documentation only; no commands were run.
