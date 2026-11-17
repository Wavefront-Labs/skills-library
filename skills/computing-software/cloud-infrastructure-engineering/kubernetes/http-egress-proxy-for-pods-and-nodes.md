---
id: computing-software.cloud-infrastructure-engineering.kubernetes.http-egress-proxy-for-pods-and-nodes
name: http-egress-proxy-for-pods-and-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, egress-proxy, http-proxy-env, no-proxy, corporate-proxy, containerd, egress-control]
level: practitioner
status: docs-checked
description: "Run Kubernetes behind a corporate HTTP proxy: containerd and kubelet proxy config, pod HTTP_PROXY/NO_PROXY that keeps in-cluster traffic direct, and per-runtime quirks."
sources: ["https://pkg.go.dev/golang.org/x/net/http/httpproxy", "https://curl.se/docs/manpage.html", "https://curl.se/libcurl/c/CURLOPT_NOPROXY.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/net/doc-files/net-properties.html", "https://nodejs.org/api/cli.html", "https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP egress proxies and proxy env vars

## Two separate layers
1. **Node layer**: containerd pulls images, kubeadm/kubelet talk to the API. Configure via systemd.
2. **Pod layer**: application traffic. Configure via container env.

## Node: containerd
```ini
# /etc/systemd/system/containerd.service.d/http-proxy.conf
[Service]
Environment="HTTP_PROXY=http://proxy.corp:3128"
Environment="HTTPS_PROXY=http://proxy.corp:3128"
Environment="NO_PROXY=localhost,127.0.0.1,10.0.0.0/8,.svc,.cluster.local,.corp,169.254.169.254"
```
Reload systemd and restart containerd (`systemctl daemon-reload && systemctl restart containerd`),
then test with a `crictl pull` of a small image. containerd is a Go program and Go's standard HTTP
proxy support reads `HTTP_PROXY`, `HTTPS_PROXY` and `NO_PROXY` from the environment; the containerd
documentation read for this review does not describe proxy configuration, so the pull test is the
check. Keep the node, pod and service CIDRs and the API server endpoint in `NO_PROXY` so cluster
traffic is not sent to the proxy.

## Pod: env vars
```yaml
env:
- {name: HTTPS_PROXY, value: "http://proxy.corp:3128"}
- {name: HTTP_PROXY,  value: "http://proxy.corp:3128"}
- {name: NO_PROXY,    value: "localhost,127.0.0.1,.svc,.svc.cluster.local,.cluster.local,10.96.0.0/12,10.244.0.0/16,kubernetes.default.svc,169.254.169.254"}
- {name: https_proxy, value: "http://proxy.corp:3128"}   # lowercase copies (curl reads http_proxy only in lower case)
- {name: http_proxy,  value: "http://proxy.corp:3128"}
- {name: no_proxy,    value: "<same as NO_PROXY>"}
```
Inject cluster-wide with a mutating admission policy (MutatingAdmissionPolicy is stable from
Kubernetes 1.36) instead of editing every chart; exclude kube-system.

## NO_PROXY must contain
- Service CIDR and pod CIDR (clients that call by IP), `.svc` / `.cluster.local` suffixes.
- The API server address (in-cluster clients use `KUBERNETES_SERVICE_HOST`, an IP).
- Cloud metadata `169.254.169.254`, so metadata calls are not sent to the proxy.
- Internal registries and corporate domains.

## Runtime quirks (cause of most incidents)
- **Case**: curl documents that `http_proxy` is only read in lower case, that `HTTPS_PROXY` works in either case, and that the lower-case form takes precedence; set both cases.
- **CIDR in NO_PROXY**: Go's httpproxy package accepts CIDR notation and curl added it in 7.86.0; other tools vary, so list key IPs explicitly where you cannot confirm CIDR support.
- **Leading dot**: in Go, `foo.com` matches `foo.com` and its subdomains, while `.foo.com` matches subdomains only; other tools differ.
- **Java** documents proxy settings as system properties: `-Dhttps.proxyHost=... -Dhttps.proxyPort=... -Dhttp.nonProxyHosts="*.svc|*.cluster.local|10.*"` (pipe-separated with `*` wildcards, not CIDR; the HTTPS handler uses the same `nonProxyHosts`), for example via `JAVA_TOOL_OPTIONS`.
- **Node.js** documents `NODE_USE_ENV_PROXY=1` (stability 1.1, active development), which makes it read `HTTP_PROXY`, `HTTPS_PROXY` and `NO_PROXY`; without it, do not assume the variables are honoured.
- TLS-inspecting proxies need the corporate CA in the image trust store or mounted.

## Verify
```bash
kubectl exec deploy/app -- sh -c 'env | grep -i _proxy'
kubectl exec deploy/app -- curl -sv https://example.com 2>&1 | grep -i 'proxy'
kubectl exec deploy/app -- curl -sv http://other.ns.svc.cluster.local 2>&1 | grep -iv proxy   # direct
```
Proxy access logs should show only external hosts, never `*.svc` names or pod IPs.

## Checked

2026-10-27. Release: Go x/net, curl, Java 21, Node.js and Kubernetes v1.37 docs, October 2026
- Confirmed in the Go httpproxy documentation that NO_PROXY accepts IP prefixes, CIDR notation and domain names, that a bare domain matches itself and subdomains while a leading dot matches subdomains only, and that the CGI case is guarded.
- Confirmed in curl documentation that `http_proxy` is read only in lower case, lower case takes precedence, and CIDR in NO_PROXY was added in 7.86.0; confirmed Java's `http.nonProxyHosts` pipe-separated wildcard format and `https.proxyHost`, and Node's `NODE_USE_ENV_PROXY=1`.
- Confirmed that pods get `KUBERNETES_SERVICE_HOST` and can use `kubernetes.default.svc` (Kubernetes access-API-from-a-pod page).
- Removed the kubeadm proxy claim, the Python requests/wget/Ruby CIDR claims and the workload-identity claim, which no source read confirmed, and stated plainly that containerd's own docs do not cover proxy settings.

Method: documentation only; no commands were run.
