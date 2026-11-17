---
id: computing-software.messaging-and-integration.dapr.app-api-token-sidecar-to-app-auth
name: app-api-token-sidecar-to-app-auth
category: computing-software
field: messaging-and-integration
product: dapr
tags: [security, app-api-token, authentication, kubernetes-secret, pubsub, service-invocation, bindings]
level: practitioner
status: docs-checked
description: "Let your app verify calls from the Dapr sidecar: APP_API_TOKEN, the dapr.io/app-token-secret annotation, the dapr-api-token header the sidecar adds, and rotation steps."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/security/app-api-token.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For building blocks where Dapr calls your app over HTTP or gRPC (pub/sub delivery, service invocation, input bindings), the app can require proof that the caller is its own sidecar. The page links a separate how-to for the opposite direction, authenticating calls to the sidecar.

Self-hosted: set `APP_API_TOKEN` before `daprd` launches and Dapr includes it on every call to the app.

```shell
export APP_API_TOKEN=<token>
```

Kubernetes:

```shell
kubectl create secret generic app-api-token --from-literal=token=<token>
```

(create it in each namespace where you enable this), then annotate the Deployment template:

```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-token-secret: "app-api-token" # name of the Kubernetes secret
```

The Sidecar Injector injects the value into `APP_API_TOKEN`.

In your app, check the incoming HTTP header `dapr-api-token: <token>`, or for gRPC the metadata entry `dapr-api-token[0]`. The token itself can be generated with `openssl rand 16 | base64`.

Rotation: update the secret per namespace (`kubectl apply --file token-secret.yaml --namespace <namespace-name>`) and run `kubectl rollout restart deployment/<deployment-name> --namespace <namespace-name>`; with several replicas there is no downtime. In self-hosted mode change `APP_API_TOKEN` and restart `daprd`.

To expose the token to the app container use `envFrom` with a `secretRef` whose name is `app-api-token`.

## Checked

2026-11-08. Environment variable, secret and annotation, header and gRPC metadata names, rotation commands and envFrom example confirmed on the Authenticate requests from Dapr using token authentication page. Changed: removed the claim about differing variables across the two token features (that is on a page not cited here). Note the page says a 32-byte key but its command is `openssl rand 16`; the skill quotes the command only.

Method: documentation only; every cited page read in full; no commands were run.
