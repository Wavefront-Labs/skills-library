---
id: computing-software.cloud-infrastructure-engineering.openbao.kubernetes-auth
name: kubernetes-auth
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, kubernetes-auth, service-account, token-reviewer, auth-delegator]
level: practitioner
status: docs-checked
description: "Authenticate Kubernetes pods to OpenBao: config keys, role bindings, the four token reviewer options and their security trade-offs."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/auth/kubernetes.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes auth

```
bao auth enable kubernetes
bao write auth/kubernetes/config kubernetes_host=... kubernetes_ca_cert=@ca.crt
bao write auth/kubernetes/role/demo \
    bound_service_account_names=myapp \
    bound_service_account_namespaces=default \
    policies=default ttl=1h
bao write auth/kubernetes/login role=demo jwt=...
```

Find the API address with `kubectl cluster-info`. The `issuer`, if needed: `kubectl get --raw /.well-known/openid-configuration | jq -r .issuer`.

## Config notes

`kubernetes_host` includes the port (in a pod, `$KUBERNETES_SERVICE_HOST` and `$KUBERNETES_SERVICE_PORT`). `disable_iss_validation` should be `true` (default for new mounts; needed for Kubernetes 1.21+). `issuer` is deprecated.

## Token reviewer options

1. **Local token** (recommended when OpenBao runs in Kubernetes): omit `token_reviewer_jwt` and `kubernetes_ca_cert`; it rereads the pod's token and CA periodically.
2. **Client JWT**: omit `token_reviewer_jwt`; each client needs the `system:auth-delegator` ClusterRole. Set `disable_local_ca_jwt=true`.
3. **Long-lived secret** as reviewer JWT: legacy, loses short-lived-token benefits.
4. **JWT auth**: verify tokens as OIDC; no reviewer JWT, but client tokens cannot be revoked before TTL.

## Warnings

- Do not share the pod's JWT with other applications.
- Short-lived reviewer tokens die with the pod or service account, then TokenReview stops working.
- Kubernetes needs service account lookup enabled, or deleted tokens may still authenticate.

## Checked

2026-11-04. Confirmed against the Kubernetes auth method page: setup commands, kubectl cluster-info and the issuer lookup, disable_iss_validation and the deprecated issuer, the four token reviewer options with their trade-offs, system:auth-delegator, disable_local_ca_jwt, and the JWT sharing and service account lookup warnings. Nothing removed.

Method: documentation only; no commands were run.
