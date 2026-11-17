---
id: computing-software.messaging-and-integration.dapr.api-token-app-to-sidecar-auth
name: api-token-app-to-sidecar-auth
category: computing-software
field: messaging-and-integration
product: dapr
tags: [security, api-token, dapr-api-token, kubernetes-secret, authentication, sidecar, self-hosted]
level: practitioner
status: docs-checked
description: "Require a shared token on Dapr sidecar APIs: DAPR_API_TOKEN, the dapr.io/api-token-secret annotation, per-namespace secret, rotation by rollout restart, dapr-api-token header."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/security/api-token.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Dapr relies on the network boundary to protect its API. Token authentication adds a shared secret that every call to the sidecar must carry. Dapr imposes no format; the page generates one with:

```sh
openssl rand 16 | base64
```

Self-hosted: if `DAPR_API_TOKEN` is set when `daprd` starts, authentication is enforced.

```shell
export DAPR_API_TOKEN=<token>
```

Kubernetes: store the token in a secret (create it in every namespace that needs it) and reference it with an annotation:

```shell
kubectl create secret generic dapr-api-token --from-literal=token=<token>
```

```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/api-token-secret: "dapr-api-token" # name of the Kubernetes secret
```

The sidecar injector builds the secret reference and injects the value into the `DAPR_API_TOKEN` environment variable.

Rotation: self-hosted, change the variable and restart `daprd`. Kubernetes, update the secret in each namespace (the page says applying a manifest, `kubectl apply --file token-secret.yaml --namespace <namespace-name>`, is simpler than `kubectl patch`) and run `kubectl rollout restart deployment/<deployment-name> --namespace <namespace-name>`. With more than one replica there is no downtime.

Clients must send the header `dapr-api-token: <token>` over HTTP, or the `dapr-api-token[0]` gRPC metadata entry. Example: `curl http://localhost:3500/v1.0/metadata --header "dapr-api-token: my-token"`. SDKs read `DAPR_API_TOKEN` and set it for you. Give the app the token with `envFrom` and `secretRef` on the same secret.

## Checked

2026-11-08. Env variable, annotation, secret, rotation, header and gRPC metadata names, curl example and SDK behaviour confirmed on the Enable API token authentication in Dapr page. Changed: removed an unsupported remark about base64 values in the manifest. Other claims unchanged.

Method: documentation only; every cited page read in full; no commands were run.
