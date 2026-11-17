---
id: computing-software.cloud-infrastructure-engineering.kubernetes.scraping-control-plane-metrics
name: scraping-control-plane-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, control-plane-scraping, prometheus-operator, kube-prometheus-stack, servicemonitor, kube-apiserver, kube-etcd, kube-proxy, kubelet, kube-scheduler, kube-controller-manager, coredns, bearer-token, tls-config, metrics, monitoring, client-certificates]
level: advanced
status: gated
description: "Scrape apiserver, scheduler, controller-manager, etcd, kube-proxy and kubelet with Prometheus Operator: bearer-token auth, kubeEtcd client certs, the kube-proxy bind fix."
sources: ["https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/README.md", "https://prometheus-operator.io/docs/", "https://kubernetes.io/docs/concepts/cluster-administration/monitoring/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scraping Kubernetes control-plane metrics

**Goal:** collect metrics from the components that *run* the cluster - apiserver, etcd, scheduler,
controller-manager, kube-proxy, kubelet - where the obstacles are authentication and TLS, not the
metrics themselves.

Control-plane components do not publish Prometheus metrics as ordinary Services you can point at.
They listen on **secure ports** requiring a bearer token (and TLS verification), which is why a
naive ServiceMonitor returns auth errors or nothing.

## kube-prometheus-stack: the built-in ServiceMonitors
The chart ships ServiceMonitors for **kubelet, kube-apiserver, kube-controller-manager,
kube-scheduler, kube-etcd, kube-proxy, coredns and kube-dns** (plus kube-state-metrics and
node-exporter as dependencies - disable with `kubeStateMetrics.enabled: false`,
`nodeExporter.enabled: false`, `grafana.enabled: false`).

## Authentication: Kubernetes objects, not filesystem files
The built-in ServiceMonitors "authenticate through Kubernetes objects rather than through files on
the scraper's filesystem": the **bearer token comes from a Secret referenced by `authorization`**,
and the **CA comes from the `kube-root-ca.crt` ConfigMap** that Kubernetes maintains in every
namespace. `prometheus.serviceAccount.createTokenSecret` (enabled by default) renders a
`kubernetes.io/service-account-token` Secret named `<prometheus-service-account>-token` and every
component references it by default:

```yaml
kubelet:
  serviceMonitor:
    authorization:
      type: Bearer
      credentials:
        name: '{{ include "kube-prometheus-stack.prometheus.tokenSecretName" . }}'
        key: token
    tlsConfig:
      insecureSkipVerify: true
      ca:
        configMap:
          name: kube-root-ca.crt
          key: ca.crt
```

Both `authorization` and `tlsConfig` accept any field of the operator's **SafeAuthorization** and
**SafeTLSConfig** types; set `authorization: null` to scrape a component without authentication.
This Secret-based design is also what keeps the ServiceMonitors valid when
`prometheus.prometheusSpec.arbitraryFSAccessThroughSMs.deny` is `true`.

## The two special cases
**kubeEtcd is the only component scraped with client certificates:**
```yaml
kubeEtcd:
  serviceMonitor:
    scheme: https
    tlsConfig:
      ca:        { secret: { name: etcd-client-cert, key: etcd-ca } }
      cert:      { secret: { name: etcd-client-cert, key: etcd-client } }
      keySecret: { secret: { name: etcd-client-cert, key: etcd-client-key } }
```

**coredns and kube-dns have no `tlsConfig` - those endpoints are scraped over HTTP.**

## The kube-proxy trap
"The metrics bind address of kube-proxy is default to `127.0.0.1:10249` that prometheus instances
**cannot** access. You should expose metrics by changing the `metricsBindAddress` field value to
`0.0.0.0:10249`" - in the `kube-system/kube-proxy` ConfigMap (field `metricsBindAddress` under
`config.conf`, in `kube-system/kube-proxy` or `kube-system/kube-proxy-config`):
```bash
kubectl -n kube-system edit cm kube-proxy
```
Then restart kube-proxy. Without this, kube-proxy scraping silently yields nothing on a default
cluster - the single most common "why is kube-proxy empty" answer.

## Discovery is CRD-based, and label-gated
The operator "does not support annotation-based discovery" - ServiceMonitor/PodMonitor CRDs are the
mechanism. By default Prometheus discovers monitors **within its namespace, labelled with the same
release tag as the operator's release**; to discover all monitors in the namespace regardless of
label, set `prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues` and
`...podMonitorSelectorNilUsesHelmValues` to `false`.

## Helm deep-merge gotcha
Replacing a default (e.g. swapping the kubelet CA from the ConfigMap to a Secret) requires
explicitly clearing the original key, or the deep merge keeps both:
```yaml
kubelet:
  serviceMonitor:
    tlsConfig:
      ca:
        configMap: null          # clear the default first
        secret: { name: kubelet-scrape-auth, key: ca.crt }
```

## Failure modes
- **kube-proxy series absent** - `metricsBindAddress` still `127.0.0.1:10249`.
- **401/403 on apiserver/scheduler/controller-manager** - no token Secret referenced, or the
  service account lacks permission; the token Secret must live in the ServiceMonitor's namespace.
- **x509 errors on etcd** - using bearer-token auth where the deployment requires client
  certificates; only kubeEtcd is client-cert by default.
- **A custom ServiceMonitor never picked up** - it lacks the release label and
  `selectorNilUsesHelmValues` is still true, or it is in the wrong namespace.
- **Chart install fails on the token Secret** - `prometheus.serviceAccount.create` or
  `prometheus.enabled` disabled while components still reference the Secret.
- **Overriding a default appends instead of replaces** - the Helm deep-merge; clear the old key
  explicitly.
- **Duplicate kubelet metrics after migration** - the chart creates a new kubelet Service; the old
  `prometheus-operator-kubelet` Service in `kube-system` must be deleted.

## Verify
- [ ] One series from each component exists (`up{job="kube-apiserver"}` et al.) - the fastest
      end-to-end check that auth and TLS both worked.
- [ ] kube-proxy metrics present after the `metricsBindAddress` change.
- [ ] The token Secret exists in the ServiceMonitors' namespace and is referenced by
      `authorization`.
- [ ] kubeEtcd scraping uses the client-certificate Secret, and coredns/kube-dns are scraped over
      HTTP by design.
- [ ] Custom ServiceMonitors are discovered (label or selector-nil setting), and every Helm
      override of a default explicitly clears the replaced key.

*Component list, Secret-based authentication, the kubeEtcd client-certificate configuration, the
coredns/kube-dns HTTP note, the kube-proxy `metricsBindAddress` fix and the deep-merge behaviour
all verified against the kube-prometheus-stack chart README on 2026-11-01. `prometheus-operator.io`
did not resolve at fetch time, so the operator-level concepts come from the chart's documentation
of them. Nothing was executed, so `status: draft`.*

## Checked

- Date: 2026-11-02.
- Confirmed against: kube-prometheus-stack chart values for TLS scraping (tlsConfig, insecureSkipVerify, ca.crt) and kubeEtcd (chart README).
- Not confirmed: subchart disable keys and the podMonitorSelectorNilUsesHelmValues path wording, plus the Prometheus Operator page which was unreachable (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
