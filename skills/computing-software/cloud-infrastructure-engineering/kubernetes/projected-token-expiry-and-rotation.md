---
id: computing-software.cloud-infrastructure-engineering.kubernetes.projected-token-expiry-and-rotation
name: projected-token-expiry-and-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-account, token-expiration, bound-service-account-token, tokenrequest]
level: practitioner
status: docs-checked
description: "How projected ServiceAccount tokens expire and rotate (expirationSeconds, kubelet refresh at 80 percent, extended legacy expiry) and making clients reload them."
sources: ["https://kubernetes.io/docs/concepts/security/service-accounts/#bound-service-account-tokens", "https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#serviceaccount-token-volume-projection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Projected token expiry and rotation

## Defaults
The automatically mounted token is a projected, bound token:
```yaml
- serviceAccountToken:
    expirationSeconds: 3607
    path: token
```
- The kubelet requests it via TokenRequest and refreshes it when 80% of its lifetime has passed
  or it is older than 24 h.
- With `--service-account-extend-token-expiration=true` (the default), the API server extends the
  token it issues for the default-mounted projected volume (requested `expirationSeconds: 3607`,
  API audience) up to one year, or `--service-account-max-token-expiration` if that is shorter.
  It records the originally requested ~1 h expiry in a `warnafter` claim, so old clients that never
  re-read the file keep working; use after that point is counted in the
  `serviceaccount_stale_tokens_total` metric and logged in an audit annotation.

## Custom audience/expiry for external systems
```yaml
volumes:
- name: vault-token
  projected:
    sources:
    - serviceAccountToken:
        audience: vault
        expirationSeconds: 600
        path: token
```
`expirationSeconds` defaults to 1 hour and must be at least 10 minutes (600 s). Only tokens for the
API server's audience that request the default 3607 s are extended; custom-audience tokens are not.

## Client behaviour
- client-go and official SDKs re-read the token file periodically: fine.
- Custom code reading the token once at startup breaks after expiry (or after a year with
  extension). Re-read on each request or on 401.

## Find stale-token clients
```bash
kubectl get --raw /metrics | grep serviceaccount_stale_tokens_total
```
Audit events for such requests carry the annotation `authentication.k8s.io/stale-token`.

## Verify
```bash
kubectl exec <pod> -- cat /var/run/secrets/kubernetes.io/serviceaccount/token | cut -d. -f2 | base64 -d 2>/dev/null | jq '{aud, exp, iat, "kubernetes.io"}'
```
`exp` minus `iat` shows the issued lifetime; `kubernetes.io.pod` shows the binding. The JWT payload
is base64url without padding, so `base64 -d` may need padding added or may report an error.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes source.
Confirmed: default projected token `expirationSeconds: 3607`; kubelet rotation at 80% of TTL or 24 hours; `--service-account-extend-token-expiration`
default true and extension to one year limited by the max-expiration flag; extension only for the default 3607 s token with API audiences
(token.go); 10-minute minimum and 1-hour default for `expirationSeconds` (core/v1 types, authentication validation); the `warnafter`
claim, `authentication.k8s.io/stale-token` audit annotation and the beta `serviceaccount_stale_tokens_total` metric (claims.go,
metrics test). Removed the unconfirmed "atomic rewrite" remark and the pod/SA annotation detail.
Method: documentation only; no commands were run.
