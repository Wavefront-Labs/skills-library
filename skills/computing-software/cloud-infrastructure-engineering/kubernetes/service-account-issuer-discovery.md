---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-account-issuer-discovery
name: service-account-issuer-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-account-security, service-account-issuer-discovery, oidc, workload-identity-federation, jwks]
level: practitioner
status: docs-checked
description: "Publish the ServiceAccount token issuer's OIDC discovery document and JWKS so external systems (cloud IAM, Vault) can verify projected tokens."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/", "https://openid.net/specs/openid-connect-discovery-1_0.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ServiceAccount issuer discovery

Projected ServiceAccount tokens are OIDC-style JWTs. External verifiers need the issuer's
discovery document and public keys.

## apiserver flags
```
--service-account-issuer=https://oidc.k8s.example.com
--service-account-jwks-uri=https://oidc.k8s.example.com/openid/v1/jwks
--service-account-key-file=/etc/kubernetes/pki/sa.pub
--service-account-signing-key-file=/etc/kubernetes/pki/sa.key
```
The apiserver serves `/.well-known/openid-configuration` and `/openid/v1/jwks`
(OIDC-compatible but not strictly OIDC-compliant documents holding only what is needed to
validate service account tokens). `--service-account-jwks-uri` overrides the `jwks_uri` in the
discovery document; like the issuer URL it must use `https`.

## Make them reachable
- Inside the cluster: RBAC already includes the ClusterRole `system:service-account-issuer-discovery`,
  bound by default to the `system:serviceaccounts` group, so pods can read the documents with their
  token. To allow unauthenticated reads of those two paths, bind it to the unauthenticated group
  (or `system:authenticated`) according to your security needs:
  ```bash
  kubectl create clusterrolebinding oidc-reviewer --clusterrole=system:service-account-issuer-discovery --group=system:unauthenticated
  ```
- For external systems that federate with the cluster (cloud IAM OIDC providers and similar),
  check the provider's requirements for how it reaches the issuer URL and keys. If the apiserver
  must not be exposed, copy both documents to a static bucket or CDN at the issuer URL:
  ```bash
  kubectl get --raw /.well-known/openid-configuration > openid-configuration
  kubectl get --raw /openid/v1/jwks > jwks
  ```
  Re-publish on signing-key rotation.

## Use
Pod token with an audience for the external system:
```yaml
volumes:
- name: aws-token
  projected:
    sources:
    - serviceAccountToken: {audience: sts.amazonaws.com, expirationSeconds: 3600, path: token}
```
The verifier checks `iss`, `aud`, `sub` (`system:serviceaccount:<ns>:<name>`) and expiry.

## Gotchas
- Changing `--service-account-issuer` invalidates existing tokens; give two `--service-account-issuer`
  flags during migration (first is used to sign, all are accepted).
- The issuer string must match exactly, including any trailing slash (OIDC Discovery requires the
  returned issuer to be identical to the issuer URL used to fetch the document).

## Verify
`curl https://oidc.k8s.example.com/.well-known/openid-configuration` returns `issuer` equal to the flag.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes bootstrap RBAC policy.
Confirmed: the discovery and JWKS paths; `--service-account-issuer` (repeatable, first signs, all accepted, v1.22+),
`--service-account-key-file`, `--service-account-signing-key-file`, `--service-account-jwks-uri` (https required); the default ClusterRole
`system:service-account-issuer-discovery` and its default binding to `system:serviceaccounts` (policy.go); projected token audience
and expiry fields. Wrong in the original: it implied the role had to be created for in-cluster reads; cloud-provider reachability
requirements were removed as unconfirmed.
Method: documentation only; no commands were run.
