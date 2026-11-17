---
id: computing-software.cloud-infrastructure-engineering.calico.monitoring-restrict-prometheus-endpoints-with-policy
name: monitoring-restrict-prometheus-endpoints-with-policy
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [prometheus, metrics, host-endpoint, globalnetworkpolicy, globalnetworkset, deny-list, calico-node, port-9091]
level: advanced
status: docs-checked
description: "Limit who can scrape Calico metrics ports using a default-allow host policy, host endpoints, a deny rule on port 9091 and an allow label for scrapers."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/comms/secure-metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two approaches exist: **deny-list** (allow all host traffic by default, then block specific ports) or an allow-list (deny by default, explicitly allow everything). The page works the deny-list example for the calico-node metrics port.

1. **Default-allow host policy first**, to avoid a connectivity drop once host endpoints exist (they default to deny):

```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: default-host
spec:
  selector: running-calico == "true"
  order: 5000
  ingress:
    - action: Allow
  egress:
    - action: Allow
```

2. List nodes with `calicoctl get nodes`, then create a HostEndpoint per node labelled `running-calico: 'true'`, with `node`, `interfaceName` and `expectedIPs`.
3. **Deny everything but labelled sources** to the metrics port:

```yaml
spec:
  selector: running-calico == "true"
  order: 500
  types:
    - Ingress
  ingress:
    - action: Deny
      protocol: TCP
      source:
        notSelector: calico-prometheus-access == "true"
      destination:
        ports:
          - 9091
```

4. Grant access by label, for example `kubectl label pod my-prometheus-pod calico-prometheus-access=true`, or a GlobalNetworkSet with that label and the scraper subnets under `nets`.

**Typha** (likely installed with the Kubernetes datastore above 50 nodes): add the same kind of policy for port 9093. **kube-controllers**: a NetworkPolicy in `calico-system` (use the namespace Calico is installed in, `kube-system` for some installs) selecting `k8s-app == "calico-kube-controllers"`, order 500, with the same Deny rule for port 9094.

**Allow-list approach.** Create the host endpoints only (this blocks all host traffic apart from Felix failsafe ports, adjustable with `failsafeInboundHostPorts` and `failsafeOutboundHostPorts`), skip the default-allow policy, and use an ingress `Allow` rule with `source.selector: calico-prometheus-access == "true"` to ports 9091, 9093 and 9094 instead of the Deny rule. You must know every host port that should stay open.

## Checked

2026-11-08. The Secure Calico Prometheus endpoints page was read in full. Steps 1 to 4 and their YAML, the Typha and kube-controllers policies and the allow-list approach were confirmed.

Method: documentation only; no commands were run.
