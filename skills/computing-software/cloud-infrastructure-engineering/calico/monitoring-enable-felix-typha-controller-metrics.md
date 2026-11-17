---
id: computing-software.cloud-infrastructure-engineering.calico.monitoring-enable-felix-typha-controller-metrics
name: monitoring-enable-felix-typha-controller-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [prometheus, metrics, felix, typha, kube-controllers, monitoring, servicemonitor, windows]
level: practitioner
status: docs-checked
description: "Turn on Prometheus metrics for Felix and Typha, know the kube-controllers default, and create the headless services for ports 9091, 9093 and 9094."
sources:
  - https://docs.tigera.io/calico/latest/operations/monitor/monitor-component-metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Felix metrics are **off** by default. Enable them:

```bash
kubectl patch felixconfiguration default --type merge --patch '{"spec":{"prometheusMetricsEnabled": true}}'
```

(`calicoctl patch felixconfiguration default --patch ...` works too.) Felix publishes on TCP 9091. Prometheus finds endpoints through a Kubernetes service, so create a headless one:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: felix-metrics-svc
  namespace: calico-system
spec:
  clusterIP: None
  selector:
    k8s-app: calico-node
  ports:
  - port: 9091
    targetPort: 9091
```

On Windows nodes add a second service selecting `k8s-app: calico-node-windows`, and set FelixConfiguration `windowsManageFirewallRules` to `Enabled` (the Windows firewall blocks listening ports by default) or add a firewall rule yourself.

**Typha** (operator installs deploy it automatically; metrics are off by default). Set the port on the Installation; the operator then creates the service itself:

```bash
kubectl patch installation default --type=merge -p '{"spec": {"typhaMetricsPort":9093}}'
```

Verify with `kubectl get svc -n calico-system calico-typha-metrics`. If you have no Typha, skip it (`kubectl get pods -A | grep typha` tells you).

**kube-controllers** metrics are enabled by default on TCP 9094 and the operator creates the `calico-kube-controllers-metrics` service.

For non-operator installs the page shows hand-written services in `kube-system`, such as `typha-metrics-svc` on port 9093.

## Checked

2026-11-04. Commands, ports, defaults and service YAML were confirmed on the Monitor Calico component metrics page. Prometheus deployment steps on the page are not covered by this skill.

Method: documentation only; no commands were run.
