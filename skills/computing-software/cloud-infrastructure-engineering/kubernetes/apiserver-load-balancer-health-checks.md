---
id: computing-software.cloud-infrastructure-engineering.kubernetes.apiserver-load-balancer-health-checks
name: apiserver-load-balancer-health-checks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, control-plane-ha, apiserver-health-checks, readyz-endpoint, haproxy, kube-vip]
level: practitioner
status: docs-checked
description: "Configure the control-plane load balancer to health-check kube-apiserver via /readyz over TLS so failed or draining API servers leave rotation."
sources: ["https://kubernetes.io/docs/reference/using-api/health-checks/", "https://github.com/kubernetes/kubeadm/blob/main/docs/ha-considerations.md", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/#anonymous-authenticator-configuration", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API server load balancer health checks

## Endpoints
| Path | Meaning | Use for |
|---|---|---|
| `/livez` | process alive | kubelet liveness of the static pod |
| `/readyz` | ready to serve (etcd reachable, informers synced, not shutting down) | load balancer health checks |
| `/healthz` | deprecated since v1.16 | avoid in new configs |

Machines that probe these endpoints should rely on the HTTP status code. Per-check paths
exist too (for example `/readyz/etcd`; see the health-checks page for the exact names).
The default `system:public-info-viewer` ClusterRole (bound to `system:authenticated` and
`system:unauthenticated`) gives read-only access to non-sensitive cluster information, so a
probe can run without credentials unless you changed that. If anonymous authentication is
disabled with `--anonymous-auth=false`, anonymous probes are rejected; instead set the
`anonymous` section of an `AuthenticationConfiguration` file (feature gate
`AnonymousAuthConfigurableEndpoints`, GA in v1.34) with `enabled: true` and `conditions`
listing only the probe paths (`/livez`, `/readyz`, `/healthz`). `--anonymous-auth` and the
`anonymous` field are mutually exclusive.

## HAProxy (TCP passthrough with HTTPS check)
```
frontend k8s-api
  bind *:6443
  mode tcp
  default_backend k8s-api
backend k8s-api
  mode tcp
  option httpchk
  http-check connect ssl
  http-check send meth GET uri /readyz
  http-check expect status 200
  balance roundrobin
  server cp1 10.0.0.11:6443 check verify none
  server cp2 10.0.0.12:6443 check verify none
  server cp3 10.0.0.13:6443 check verify none
```
This follows the HAProxy example in the kubeadm HA-considerations document, which probes
`/healthz`; `/readyz` is substituted here because `/healthz` is deprecated. Keep the
frontend in TCP mode (stream load balancing): the kubeadm document notes this lets the
API server instances handle TLS termination themselves. Tune check intervals with HAProxy's
own documentation.

## Cloud LBs
- The kubeadm HA guide's cloud example uses a TCP check on the API server port (default
  6443) behind a TCP-forwarding load balancer; an HTTPS check of `/readyz` additionally
  removes a backend whose process is up but not ready. Check your provider's documentation
  for the health-check settings.
- kube-vip runs as a static pod and implements both virtual IP management and load
  balancing, either layer 2 (ARP, with leader election) or layer 3 (BGP).

## Graceful shutdown
`kube-apiserver --shutdown-delay-duration` keeps the server running while `/readyz` already
reports failure, so the LB can drain it before connections are cut. Set it longer than the
time your health check needs to mark a backend down (for HAProxy, `fall` x `inter`).

## Verify
```bash
curl -k https://10.0.0.11:6443/readyz?verbose
# stop one apiserver (move its manifest out of /etc/kubernetes/manifests), watch the LB mark it down,
# and confirm `kubectl get --raw /readyz` through the VIP keeps succeeding
```

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and the kubeadm HA-considerations document: health-checks page (healthz deprecated since v1.16, readyz and shutdown-delay-duration), kubeadm HA-considerations HAProxy and kube-vip sections, RBAC reference (system:public-info-viewer), authentication page (anonymous configuration) and the AnonymousAuthConfigurableEndpoints gate (GA in v1.34). Removed the unverified cloud load balancer settings and the kube-vip lb_enable flag.

Method: documentation only; no commands were run.
