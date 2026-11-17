---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventbus-jetstream-exotic
name: argo-events-eventbus-jetstream-exotic
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, jetstream, jetstreamexotic, nats, tls, accesssecret, external]
level: advanced
status: docs-checked
description: "Point Argo Events at an existing NATS JetStream cluster with jetstreamExotic, including password-secret auth, TLS secrets and streamConfig overrides."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventbus/jetstream.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventbus jetstream exotic

To use a NATS JetStream service you already run instead of one managed by Argo Events, use `jetstreamExotic`; Argo Events connects as a client.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: EventBus
metadata:
  name: default
spec:
  jetstreamExotic:
    url: nats://my-nats-server:4222
    accessSecret:
      name: nats-auth
      key: password
    streamConfig: ""
```

Authentication: `accessSecret` references a Kubernetes Secret whose key holds the NATS password or token as a plain string; Argo Events then uses basic (password) authentication. Create it with `kubectl create secret generic nats-auth --from-literal=password=<value> -n argo-events`. Omit `accessSecret` entirely if the server needs no authentication, for example behind a service mesh providing mTLS or in development.

TLS: set `tls` with `caCertSecret`, `clientCertSecret` and `clientKeySecret`, each a `name` and `key` pointing at a Secret (for example `ca.crt`, `tls.crt`, `tls.key`).

Stream configuration: `streamConfig` overrides the default JetStream stream settings such as retention policy and max age; leave it empty to use Argo Events defaults. See the NATS stream configuration documentation for the options.

## Checked

2026-11-04. Confirmed against the EventBus Jetstream page, Exotic section: `jetstreamExotic` with `url`, `accessSecret`, `streamConfig`, basic (password) authentication from the Secret key, the `kubectl create secret generic nats-auth` example, omitting `accessSecret` when no authentication is needed, the `tls` secrets and the `streamConfig` override. Nothing removed.
Method: documentation only; no commands were run.
