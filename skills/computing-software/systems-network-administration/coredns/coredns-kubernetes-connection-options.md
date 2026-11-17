---
id: computing-software.systems-network-administration.coredns.coredns-kubernetes-connection-options
name: coredns-kubernetes-connection-options
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, kubernetes, kubeconfig, tls, api-server]
level: advanced
status: docs-checked
description: "Connect the kubernetes plugin to a remote API server with endpoint, tls or kubeconfig and rate limit its API calls."
sources:
  - https://coredns.io/plugins/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run CoreDNS outside the cluster or constrain API load.

Options:
- `endpoint URL`: remote API endpoint. If omitted, connects in-cluster via the service account. Needs `tls` for clusters with authentication. Ignored when kubeconfig is set.
- `tls CERT KEY CACERT`: certificate files for the remote connection; ignored when connecting in-cluster.
- `kubeconfig KUBECONFIG [CONTEXT]`: authenticates with a kubeconfig file (TLS, username and password or token). Without CONTEXT the current context is used. The cluster address in the kubeconfig is preferred.
- `apiserver_qps QPS`: maximum request rate to the API server.
- `apiserver_burst BURST`: maximum burst size above the QPS limit.
- `apiserver_max_inflight MAX`: cap on concurrent in-flight requests.

Example outside the cluster:

```
kubernetes cluster.local {
    endpoint https://k8s-endpoint:8443
    tls cert key cacert
}
```

Startup: CoreDNS delays serving up to 5 seconds while it connects and syncs watches. After that it serves while syncing continues, answering SERVFAIL for Kubernetes records not yet synchronised. `startup_timeout DURATION` changes the 5s wait for the informer cache. Readiness is reported to the ready plugin after the sync.

## Checked

2026-11-08. Read the kubernetes plugin README in full. Option semantics, the 5s startup wait and SERVFAIL behaviour, and the remote example match it.

Method: documentation only; no commands were run.
