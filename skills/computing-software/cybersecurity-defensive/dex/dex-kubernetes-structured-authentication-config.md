---
id: computing-software.cybersecurity-defensive.dex.dex-kubernetes-structured-authentication-config
name: dex-kubernetes-structured-authentication-config
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [kubernetes, authenticationconfiguration, jwt, claimmappings]
level: advanced
status: docs-checked
description: "Use Kubernetes AuthenticationConfiguration (v1.30+) with a jwt issuer entry for Dex, claimMappings and userValidationRules."
sources:
  - https://dexidp.io/docs/guides/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From Kubernetes v1.30 you can use a structured authentication file instead of `--oidc-*` flags. Create a configuration file:

```yaml
apiVersion: apiserver.config.k8s.io/v1beta1
kind: AuthenticationConfiguration
jwt:
- issuer:
    url: https://dex.example.com:32000
    audiences:
    - example-app
    certificateAuthority: <base64 of the CA PEM>
  claimMappings:
    username:
      claim: email
    groups:
      claim: groups
  userValidationRules:
  - expression: "!user.username.startsWith('system:')"
    message: "username cannot use reserved system: prefix"
```

Then start `kube-apiserver` with `--authentication-config=/path/to/config`.

Details:

- `apiVersion` can end in `v1`, `v1beta1` or `v1alpha1` depending on your Kubernetes version.
- `audiences` lists the accepted client ids (`example-app` in the docs example).
- `certificateAuthority` is the base64 of the Dex CA, produced with `cat /etc/ssl/certs/openid-ca.pem | base64 -w0`. The docs show it inline.
- `userValidationRules`: the example rejects usernames that start with `system:`.

Gotcha: the docs present this as one of two options for connecting Dex, the other being the `--oidc-*` flags.

The API server checks the token signature and expiry, then validates the `aud` and `iss` claims before it reads subject attributes from the claims.

## Checked
2026-11-09: read the Dex Kubernetes Authentication guide in full; the config example, v1.30 availability, `--authentication-config` flag, apiVersion note and token validation steps match. Removed the CEL claim (not on the page).
Method: documentation only; no commands were run.
