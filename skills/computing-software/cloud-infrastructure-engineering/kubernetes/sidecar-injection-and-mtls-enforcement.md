---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sidecar-injection-and-mtls-enforcement
name: sidecar-injection-and-mtls-enforcement
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-mesh, istio, envoy, sidecar, iptables, mtls, peerauthentication, destinationrule, spiffe, spire, citadel, istiod, strict-mtls, traffic-encryption, linkerd]
level: advanced
status: docs-checked
description: "How sidecar injection rewires pod networking (iptables redirect) and how Istio mTLS/PeerAuthentication actually enforces encryption, with failure modes."
sources: ["https://istio.io/latest/docs/ops/deployment/application-requirements/", "https://istio.io/latest/docs/setup/additional-setup/pod-security-admission/", "https://istio.io/latest/docs/tasks/security/authentication/mtls-migration/", "https://istio.io/latest/docs/ops/configuration/traffic-management/tls-configuration/", "https://istio.io/latest/docs/concepts/security/", "https://linkerd.io/2/features/automatic-mtls/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sidecar injection and mTLS enforcement: how it actually plumbs together

**Goal:** know exactly what the sidecar injector changes about a pod's network namespace,
why that breaks certain workloads, and how to reason about mTLS enforcement instead of
treating `PeerAuthentication: STRICT` as a magic switch. Istio-flavoured (the dominant
sidecar mesh); Linkerd equivalents noted inline. Traffic-shaping on top of this (canary,
mirroring, circuit-breaking) is `istio-traffic-management-virtualservice-destinationrule`.
Sidecar-less alternatives are `istio-ambient-mode-ztunnel-waypoint` and
`cilium-service-mesh-sidecar-free`.

## 1. What injection actually does to a pod
`kubectl label namespace <ns> istio-injection=enabled` (or the `istio.io/rev` revision
label; `istio-injection` wins if both are set) makes the mutating webhook add, on pod
creation:
- An `istio-init` container that installs `iptables` rules redirecting inbound traffic to
  Envoy port `15006` and outbound traffic to `15001`. Traffic from the proxy's own user ID
  (`1337`, reserved: do not run applications as UID 1337) is not captured, and ports and
  CIDRs can be excluded (for example `traffic.sidecar.istio.io/excludeInboundPorts` and
  `excludeOutboundPorts`). The interception mode is `REDIRECT` or `TPROXY`
  (`sidecar.istio.io/interceptionMode`).
- An `istio-proxy` (Envoy) sidecar in the same network namespace. Every packet to or from
  the app detours through its own Envoy and, for in-mesh peers, the peer's Envoy.
  `istioctl proxy-config listener <pod>` shows the listeners, including `virtualOutbound`
  (15001) and the inbound listener on 15006.

**Gotchas that bite in production:**
- **The init container needs `NET_ADMIN` and `NET_RAW`.** Pod Security `baseline` does not
  allow them, so enforcing `baseline` on a mesh namespace blocks injected pods. Istio's
  documented fix is the Istio CNI plugin (`istio-cni-node` DaemonSet; its namespace must
  allow the `privileged` level because of its `hostPath` volumes), which removes the
  need for the init container's capabilities. Under `restricted`, also set a
  `seccompProfile` for your containers.
- **App container starts before the proxy is ready**: connection failures on startup for
  apps that call out immediately. Set the proxy config `holdApplicationUntilProxyStarts:
  true` (mesh-wide in `meshConfig.defaultConfig`, or per workload via the
  `proxy.istio.io/config` annotation). Native sidecars (default from Istio 1.27 where the
  cluster supports them, controllable with `sidecar.istio.io/nativeSidecar`) also start
  the proxy first.
- **Shutdown ordering**: `terminationDrainDuration` is how long the proxy keeps draining
  after SIGTERM before Envoy is killed (default 5s per the proxy config reference); an app
  that needs longer to finish outbound calls during rolling updates needs a longer value
  or native sidecars.
- **Traffic Envoy does not parse**: set `excludeOutboundPorts`/`excludeInboundPorts` for
  ports whose traffic should bypass the proxy, instead of fighting it.

## 2. mTLS: what "automatic" actually means
`istiod` includes a CA that validates each proxy's certificate signing request and issues
workload certificates, delivered to Envoy over the secret discovery service (SDS) and
refreshed periodically. The identity is derived from the workload's service account (a
SPIFFE ID of the form `spiffe://<trust-domain>/ns/<ns>/sa/<serviceaccount>`; the trust
domain defaults to `cluster.local`). No app code change: the handshake happens
proxy-to-proxy.

- **`PeerAuthentication`** controls what the *server-side* sidecar accepts: `STRICT` (mTLS
  only), `PERMISSIVE` (mTLS or plaintext) or `DISABLE`. Istio's default is `PERMISSIVE`,
  which is the safe migration state.
- **`DestinationRule.trafficPolicy.tls.mode`** controls what the *client-side* proxy
  sends; `DISABLE` sends plaintext, while `SIMPLE`, `MUTUAL` and `ISTIO_MUTUAL` originate TLS.
  With **auto mTLS**, if no TLS settings are configured in a `DestinationRule` the sidecar
  sends Istio mutual TLS to destinations that support it, so a `DestinationRule` is only
  needed to override that. A `STRICT` server reached by a client that sends plaintext
  (explicit `DISABLE` in a `DestinationRule`, or a workload with no sidecar) fails the
  connection.
- **Safe migration order** (Istio's mTLS migration task): leave `PERMISSIVE` as the default,
  check which workloads still send plaintext to workloads in `PERMISSIVE` mode (the task
  uses the Grafana dashboard), then switch to `STRICT`, namespace by namespace,
  narrowest first.
- **mTLS is not authorization.** It proves peer identity; it does not stop pod A calling
  pod B's API. That is `AuthorizationPolicy` (ALLOW/DENY by source principal).
- **Non-mesh traffic** (an ingress gateway terminating TLS, an unmeshed pod, a VM) is
  plaintext at the mesh boundary unless the gateway originates TLS to the backend; a gateway
  has independent downstream and upstream TLS settings.
- **Linkerd equivalent**: Linkerd automatically enables mutual TLS for traffic between
  meshed pods (its docs list which traffic is covered), with short-lived certificates
  issued by its identity service; there is no `PeerAuthentication` resource to configure.
  Check the Linkerd docs for the traffic types it does not cover and for trust-anchor expiry.

## 3. Diagnosing broken sidecar traffic
```bash
istioctl proxy-status                       # SYNCED / NOT SENT / STALE per proxy
istioctl proxy-config listener <pod>        # listeners actually programmed
istioctl proxy-config secret <pod>          # certificates loaded by the proxy
istioctl x describe pod <pod>               # effective PeerAuthentication and mTLS mode
istioctl x authz check <pod>                # AuthorizationPolicy applied to the pod
kubectl logs <pod> -c istio-proxy --tail=50 # Envoy access log: response flags
```
`istioctl x authz check` reports AuthorizationPolicy only; use `istioctl x describe pod` for
the effective mTLS mode. Debug the proxy log before the app: connection failures
at the proxy usually mean a TLS mismatch or a dropped connection before the app saw it.

## Verify
- [ ] `istioctl proxy-status` shows `SYNCED` for every proxy (`STALE` means an update was
  sent without an acknowledgement).
- [ ] `PeerAuthentication` mode and any explicit `DestinationRule` TLS modes agree per
  namespace (no `STRICT` server paired with a client forced to `DISABLE`).
- [ ] A plaintext `curl` from outside the mesh to a `STRICT` pod is refused.
- [ ] Rolling a Deployment produces zero "connection reset" log lines during the rollout
  window (checks sidecar start/stop ordering).

## Checked
2026-10-27. Documentation releases: istio.io docs (main), istio/api (annotations and proxy config reference), Istio 1.27 and 1.31.3 release notes and istioctl source, Linkerd website docs (2-edge).
Confirmed: ports 15001/15006, UID 1337, exclusion annotations and interception mode, `NET_ADMIN`/`NET_RAW`, PSA and CNI guidance, `holdApplicationUntilProxyStarts`, native sidecar default and annotation, `terminationDrainDuration` default, `PeerAuthentication` modes and PERMISSIVE default, auto mTLS, `DestinationRule` TLS modes, migration order, `istioctl x describe`/`x authz check` scope, SPIFFE ID format in Istio's own examples, Linkerd automatic mTLS.
Method: documentation only; no commands were run.
