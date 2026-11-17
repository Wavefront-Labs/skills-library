---
id: computing-software.cloud-infrastructure-engineering.kubernetes.aggregated-api-servers-build-and-troubleshoot
name: aggregated-api-servers-build-and-troubleshoot
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, aggregation-layer, apiservice, faileddiscoverycheck, apiservice-unavailable, requestheader-client-ca, sample-apiserver, extension-api-server-build, front-proxy]
level: advanced
status: docs-checked
description: "Build an extension API server (sample-apiserver/apiserver-runtime) behind an APIService and fix FailedDiscoveryCheck, front-proxy certificate and unavailable APIService errors."
sources: ["https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/", "https://kubernetes.io/docs/tasks/extend-kubernetes/configure-aggregation-layer/", "https://github.com/kubernetes/sample-apiserver"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Aggregated API servers: build and troubleshoot

## When to aggregate instead of a CRD
Only when you need what CRDs can't do: non-etcd storage (metrics-server serves live data),
custom subresources/verbs, protobuf, or very high write rates. Otherwise CRDs win (no server to
run, no availability coupling).

## Building
Start from `k8s.io/sample-apiserver` (uses `k8s.io/apiserver` library; same generic machinery
as kube-apiserver: authn delegation, authz via SubjectAccessReview, admission, OpenAPI).
- Delegated auth: your server reads `extension-apiserver-authentication` ConfigMap in
  kube-system and needs RBAC `system:auth-delegator` (TokenReview/SubjectAccessReview) and
  `extension-apiserver-authentication-reader` (Role in kube-system).
- Register:
```yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata: {name: v1alpha1.wardle.example.com}
spec:
  group: wardle.example.com
  version: v1alpha1
  groupPriorityMinimum: 1000
  versionPriority: 15
  service: {name: wardle-api, namespace: wardle, port: 443}
  caBundle: <base64 PEM CA bundle that signs the server's serving cert>   # insecureSkipTLSVerify: true disables verification; avoid in production
```

## The aggregation layer's own requirements (kube-apiserver flags)
```
--requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
--requestheader-allowed-names=front-proxy-client
--requestheader-extra-headers-prefix=X-Remote-Extra-
--requestheader-group-headers=X-Remote-Group
--requestheader-username-headers=X-Remote-User
--proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
--proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
--enable-aggregator-routing=true      # when apiserver can't reach Service ClusterIPs (no kube-proxy on CP)
```
Run kube-apiserver with a `--requestheader-client-ca-file` that differs from `--client-ca-file`;
the Kubernetes docs warn that sharing one CA breaks client authentication. The APIService
`service.port` is optional and defaults to 443.

## Troubleshooting
```bash
kubectl get apiservice                                # AVAILABLE False?
kubectl get apiservice v1beta1.metrics.k8s.io -o jsonpath='{.status.conditions}'
```
| `Available` condition reason | Cause |
|---|---|
| `FailedDiscoveryCheck ... the server is currently unable to handle the request` / `context deadline exceeded` | apiserver can't reach the Service: no endpoints, NetworkPolicy, control plane without pod network route (use `--enable-aggregator-routing` or hostNetwork) |
| `ServiceNotFound` / `ServicePortError` / `EndpointsNotFound` / `MissingEndpoints` | Service name/namespace/port wrong, no EndpointSlices or no ready addresses for the port |
| `x509: certificate signed by unknown authority` | wrong `caBundle` |
| backend logs `Unauthorized` / `forbidden: User "system:anonymous"` | front-proxy CA/allowed-names mismatch; backend can't read `extension-apiserver-authentication` |
An unavailable APIService leaves that group's discovery failing, which can show up as
errors from `kubectl api-resources` and from controllers that enumerate all API groups.
Delete stale APIServices of uninstalled add-ons.

## Checked
Checked 2026-10-24 against the kubernetes/website "Configure the Aggregation Layer" page (current
source), the kube-aggregator `remote_available_controller.go` source (condition reasons
`ServiceNotFound`, `ServicePortError`, `EndpointsNotFound`, `MissingEndpoints`, `FailedDiscoveryCheck`),
and the `apiregistration.k8s.io/v1` types (`port` defaults to 443, `insecureSkipTLSVerify`).
Confirmed: the `--requestheader-*` and `--proxy-client-*` flags, the
`extension-apiserver-authentication-reader` Role and `system:auth-delegator` ClusterRole, the
APIService fields, and `--enable-aggregator-routing`.
Method: documentation only; no commands were run.

## Verify
- [ ] `kubectl get apiservice` all `True`; `kubectl get --raw /apis/wardle.example.com/v1alpha1` returns a resource list.
