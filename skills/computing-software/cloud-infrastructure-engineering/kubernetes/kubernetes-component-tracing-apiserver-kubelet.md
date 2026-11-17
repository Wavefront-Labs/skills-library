---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubernetes-component-tracing-apiserver-kubelet
name: kubernetes-component-tracing-apiserver-kubelet
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, apiserver-tracing, tracingconfiguration, kubelet-tracing, opentelemetry, otlp, etcd, control-plane]
level: advanced
status: docs-checked
description: "Turn on OpenTelemetry tracing in kube-apiserver, kubelet and etcd with TracingConfiguration, ship spans to a node-local collector, and use them to find slow requests."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/system-traces/", "https://kubernetes.io/docs/reference/config-api/apiserver-config.v1/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/", "https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes component tracing
Answers "why did this `kubectl apply` take 4 s?" or "where does pod startup time go?"
with spans across the apiserver, admission webhooks, etcd and kubelet/CRI.

Kubernetes components export traces with built-in OTLP gRPC exporters, by default to
`localhost:4317` (the IANA OpenTelemetry port). You can send them to an OpenTelemetry Collector or,
by setting `endpoint` in the tracing configuration, straight to a backend with no collector.
Backend auth headers can be given through `OTEL_EXPORTER_OTLP_HEADERS`.

## kube-apiserver
```yaml
# /etc/kubernetes/tracing-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: TracingConfiguration
# endpoint: localhost:4317        # default value
samplingRatePerMillion: 100       # 1 in 10000 requests; raise temporarily while investigating
```
Start kube-apiserver with `--tracing-config-file=/etc/kubernetes/tracing-config.yaml` (for a
static pod, also mount the file). Feature gate `APIServerTracing`: beta and on by default 1.27 to
1.33, stable from 1.34. The apiserver generates spans for incoming HTTP requests and for
outgoing requests to webhooks, etcd and re-entrant requests, and propagates W3C Trace Context on
outgoing requests, **but does not use trace context attached to incoming requests** (it is often a
public endpoint). So you cannot force-sample one request by sending a `traceparent` header; raise
`samplingRatePerMillion` instead.

## kubelet
```yaml
# KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
tracing:
  # endpoint: localhost:4317        # default value
  samplingRatePerMillion: 100
```
Feature gate `KubeletTracing`: beta and on by default 1.27 to 1.33, stable (locked on) from 1.34.
The kubelet instruments its CRI interface and authenticated HTTP servers, and collects spans from
garbage collection, the pod sync routine and every gRPC method. It propagates trace context on gRPC
calls so runtimes with tracing instrumentation (the docs name CRI-O and containerd) can link their
spans to the kubelet's. A parent span's sampling decision is always respected; the configured rate
applies to spans without a parent. A `samplingRatePerMillion` of 1000000 sends every span.

## etcd
etcd has its own flags (shown in `etcd --help` for current releases): `--enable-distributed-tracing`
(default false), `--distributed-tracing-address` (default `localhost:4317`),
`--distributed-tracing-service-name` (default `etcd`), `--distributed-tracing-instance-id` and
`--distributed-tracing-sampling-rate` (default 0). Older etcd releases used different,
experimental-prefixed flag names; check the help for your etcd version.

## Collector placement
Components export to `localhost:4317` by default, so the collector must be reachable there from
each host or from the component's pod (a collector as a sidecar is one documented layout). Whatever
you choose, start it before the components or accept dropped spans.

## Using it
- Look for long spans on webhook calls (a slow admission webhook) and on etcd requests.
- Keep sampling low; the Kubernetes docs note that exporting spans always has a small CPU and
  networking overhead, and recommend lowering `samplingRatePerMillion` or removing the configuration
  if it causes problems.

## Gotchas
- Managed clusters do not generally expose apiserver flags; check your provider's documentation for
  which components you can configure.
- Tracing configuration is per component: apiserver via `--tracing-config-file`, kubelet via the
  `tracing` field of `KubeletConfiguration`, etcd via its own flags.

## Verify
- [ ] Your tracing backend shows spans from the apiserver and the kubelet after a pod is created.

## Checked
Checked 2026-10-24 against the kubernetes/website "Traces For Kubernetes System Components" page
(default endpoint 4317, `--tracing-config-file`, `apiserver.config.k8s.io/v1` TracingConfiguration,
kubelet `tracing` field, apiserver ignores incoming trace context, sampling and overhead notes), the
`APIServerTracing` and `KubeletTracing` feature gate pages (beta 1.27, stable 1.34) and etcd's help
text (`--enable-distributed-tracing` and related flags, etcd v3.7.x help).
Removed: the `traceparent` force-sampling recipe (the docs say the apiserver ignores incoming trace
context), containerd plugin and collector DaemonSet specifics, and `service.name` values that no checked
documentation covers.
Method: documentation only; no commands were run.
