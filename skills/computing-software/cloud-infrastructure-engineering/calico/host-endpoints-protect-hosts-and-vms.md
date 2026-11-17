---
id: computing-software.cloud-infrastructure-engineering.calico.host-endpoints-protect-hosts-and-vms
name: host-endpoints-protect-hosts-and-vms
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [host-endpoint, globalnetworkpolicy, host-protection, felix, defaultendpointtohostaction, failsafe, vm]
level: practitioner
status: docs-checked
description: "Protect hosts and VMs with a HostEndpoint plus GlobalNetworkPolicy, and control workload-to-host traffic with defaultEndpointToHostAction."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/hosts/protect-hosts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A host is a node or VM; its network interfaces are secured as host endpoints, which carry labels and are selected by policy like workload endpoints.

**Defaults to know.**
- Once a HostEndpoint exists with no policy, traffic to or from it is denied, except what the failsafe rules allow.
- Calico blocks connections from a workload to its local host by default.
- Calico allows all connections from host processes to workloads on the host (kubelet health checks depend on it). It does not protect a workload from its own host.

**Step 1: policy for the hosts** (a GlobalNetworkPolicy selecting by label):

```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: k8s-worker
spec:
  selector: "role == 'k8s-worker'"
  order: 0
  ingress:
    - action: Allow
      protocol: TCP
      source:
        nets:
          - '<your management CIDR>'
      destination:
        ports: [22]
    - action: Allow
      protocol: ICMP
```

The page's full example also allows TCP 10250 in, and etcd, DNS and DHCP out.

**Step 2: one HostEndpoint per interface.** `node` must match the hostname on the Calico Node object:

```yaml
apiVersion: projectcalico.org/v3
kind: HostEndpoint
metadata:
  name: my-host-eth0
  labels:
    role: k8s-worker
spec:
  interfaceName: eth0
  node: my-host
  expectedIPs: ['10.0.0.1']
```

**Workload-to-host.** Set `defaultEndpointToHostAction` in the default FelixConfiguration to Drop (default), Accept or Return; it works at the iptables level. Edit by exporting with `calicoctl get felixconfiguration default --export -o yaml`, then `calicoctl apply -f`.

## Checked

Read in full on 2026-11-08: the Protect hosts and VMs page. Default behaviours, both YAML resources and the FelixConfiguration edit steps match it.

Method: documentation only; no commands were run.
