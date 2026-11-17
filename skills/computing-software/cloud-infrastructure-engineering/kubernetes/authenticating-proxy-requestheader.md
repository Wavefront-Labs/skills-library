---
id: computing-software.cloud-infrastructure-engineering.kubernetes.authenticating-proxy-requestheader
name: authenticating-proxy-requestheader
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, authentication, authenticating-proxy, requestheader-auth, front-proxy, kube-apiserver]
level: practitioner
status: docs-checked
description: "Put an authenticating proxy in front of kube-apiserver using requestheader flags, client-cert trust and header stripping, without opening an impersonation hole."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/authentication/#authenticating-proxy", "https://kubernetes.io/docs/setup/best-practices/certificates/", "https://kubernetes.io/docs/tasks/extend-kubernetes/configure-aggregation-layer/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authenticating proxy (requestheader auth)

The proxy authenticates the user (SSO, VPN, etc), then calls the apiserver with a client
certificate and headers naming the user. The apiserver trusts the headers only when the
request carries a cert signed by the requestheader CA with an allowed CN.

## apiserver flags
```
--requestheader-client-ca-file=/etc/kubernetes/pki/proxy-ca.crt
--requestheader-allowed-names=auth-proxy
--requestheader-username-headers=X-Remote-User
--requestheader-group-headers=X-Remote-Group
--requestheader-extra-headers-prefix=X-Remote-Extra-
```
`--requestheader-uid-headers` also exists, but it needs the alpha feature gate `RemoteRequestHeaderUID` (added in v1.32, off by default).

## Proxy must
- Strip any incoming `X-Remote-*` headers from clients before adding its own.
- Present its client cert (CN `auth-proxy`) on every upstream request.
- Use a separate CA from the cluster CA and from `front-proxy-ca` used by the aggregation layer,
  or restrict `allowed-names` so the aggregator cert cannot be reused.

## Gotchas
- If `--requestheader-allowed-names` is empty, any CN is allowed, so any cert signed by that CA
  can assert any user and group, including `system:masters`. Always set it.
- The aggregation layer already uses `--requestheader-client-ca-file` with the front-proxy CA and a
  `front-proxy-client` certificate (kubeadm PKI layout); adding your proxy means a second trusted
  name or a shared CA, and the docs warn against trusting a CA that is used in another context.
  Prefer OIDC or structured authentication for humans unless you really need a proxy.

## Verify
```bash
curl --cert proxy.crt --key proxy.key --cacert ca.crt \
  -H 'X-Remote-User: alice' -H 'X-Remote-Group: dev' \
  https://<apiserver>:6443/apis/authentication.k8s.io/v1/selfsubjectreviews -X POST \
  -H 'Content-Type: application/json' -d '{"apiVersion":"authentication.k8s.io/v1","kind":"SelfSubjectReview"}'
```
The response must show `alice` and `dev`; the same request without the cert must be anonymous or rejected.

## Checked

Checked 2026-10-27 against Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time).

- Flag semantics confirmed in the authentication page: `--requestheader-client-ca-file` is required, `--requestheader-allowed-names` empty means any CN, username/group/extra header behaviour.
- `--requestheader-uid-headers` confirmed in kube-apiserver source as gated by feature gate `RemoteRequestHeaderUID` (alpha, default false, from v1.32).
- SelfSubjectReview API confirmed in the authentication page; front-proxy CA and client certificate layout confirmed in the PKI page.

Method: documentation only; no commands were run.
