---
id: computing-software.cloud-infrastructure-engineering.kubernetes.structured-authentication-and-webhook-token-auth
name: structured-authentication-and-webhook-token-auth
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, authentication, authenticationconfiguration, webhook-token-authentication, aws-iam-authenticator, structured-authentication, jwt-authenticator, cel]
level: advanced
status: docs-checked
description: "Configure structured AuthenticationConfiguration (multiple JWT issuers, CEL claim mappings, hot reload) and webhook token authentication such as aws-iam-authenticator."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/authentication/#using-authentication-configuration", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/#webhook-token-authentication", "https://github.com/kubernetes-sigs/aws-iam-authenticator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured authentication config and webhook token auth

## AuthenticationConfiguration (alpha 1.29, beta 1.30, GA 1.34)
Replaces `--oidc-*` flags; supports **several issuers**, CEL claim validation/mapping, and
reloads the authenticators automatically when the file changes. Pass
`--authentication-config=<file>`; combining it with any `--oidc-*` flag is not allowed, so remove
those flags when you switch.
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AuthenticationConfiguration
jwt:
- issuer:
    url: https://keycloak.example.com/realms/k8s
    audiences: [kubernetes]
  claimValidationRules:
  - expression: 'claims.email_verified == true'
    message: email must be verified
  claimMappings:
    username: {expression: '"oidc:" + claims.email'}
    groups: {expression: 'claims.groups.map(g, "oidc:" + g)'}
    uid: {claim: sub}
  userValidationRules:
  - expression: "!user.username.startsWith('system:')"
    message: username cannot use reserved prefix
- issuer:
    url: https://token.actions.githubusercontent.com
    audiences: [my-cluster]
  claimMappings:
    username: {expression: '"gha:" + claims.repository + ":" + claims.ref'}
```
Static-pod: mount the file into the apiserver pod (hostPath) — the path must exist inside
the container. The metric
`apiserver_authentication_config_controller_automatic_reload_last_timestamp_seconds` shows when
the configuration was last reloaded (the controller also exposes `automatic_reloads_total`).

## Webhook token authentication
The apiserver POSTs a `TokenReview` to an external service for bearer tokens it cannot
verify itself.
```bash
--authentication-token-webhook-config-file=/etc/kubernetes/authn-webhook.kubeconfig
--authentication-token-webhook-cache-ttl=2m
--authentication-token-webhook-version=v1
```
The config is a kubeconfig whose `cluster.server` is the webhook URL and `users` are the
client cert the apiserver presents. Response:
`{"apiVersion":"authentication.k8s.io/v1","kind":"TokenReview","status":{"authenticated":true,"user":{"username":"...","groups":[...]}}}`.

**aws-iam-authenticator** (kubernetes-sigs project; a webhook token authenticator for AWS IAM
identities): it maps IAM roles and users to Kubernetes usernames and groups using its server
configuration file, an EKS-style `aws-auth` ConfigMap (`--backend-mode=EKSConfigMap`) or
`IAMIdentityMapping` custom resources (`--backend-mode=CRD`, alpha). On EKS, AWS provides access
entries (`aws eks create-access-entry`) as an alternative to editing `aws-auth`.

## Gotchas
- Webhook down = those users cannot authenticate; the cache TTL is your outage buffer. Run it
  HA, on host network, not dependent on the cluster it authenticates.
- When several authenticators are enabled, the first one that authenticates the request wins, and
  the API server does not guarantee the order they run in.
- A single JWT issuer URL cannot appear twice in AuthenticationConfiguration.

## Verify
- [ ] `kubectl auth whoami` for each issuer's identity returns mapped username/groups.
- [ ] Editing the config file is picked up (reload metric increments) without restart.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37), kubernetes/kubernetes source and the aws-iam-authenticator README.
Confirmed: `StructuredAuthenticationConfiguration` gate stages (alpha 1.29, beta 1.30, stable 1.34); `apiserver.config.k8s.io/v1`
AuthenticationConfiguration with `jwt[].issuer.url` and `audiences`, `claimValidationRules` (claim/requiredValue or CEL expression),
`claimMappings` username/groups/uid (claim or expression), `userValidationRules`; unique issuer URL per authenticator; no mixing with
`--oidc-*` flags; automatic reload and the `..._automatic_reload_last_timestamp_seconds` metric; webhook flags
`--authentication-token-webhook-config-file`, `--authentication-token-webhook-cache-ttl` (default 2 minutes) and
`--authentication-token-webhook-version`; authenticator order not guaranteed. Wrong in the original: AuthenticationConfiguration shown as
`v1beta1` (it is `v1` now), a fixed authenticator order, "bad file keeps last good config" (removed, unconfirmed), and the presigned-STS
description (removed, unconfirmed).
Method: documentation only; no commands were run.
