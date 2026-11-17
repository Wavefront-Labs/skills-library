---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hostport-usage-and-conflicts
name: hostport-usage-and-conflicts
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, daemonset, hostport, didnt-have-free-ports, cni]
level: practitioner
status: docs-checked
description: "Use hostPort correctly: CNI portmap requirement, scheduling conflicts, hostIP binding, why hostNetwork differs, and security implications."
sources: ["https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/#support-hostport", "https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/scheduler/framework/plugins/nodeports/node_ports.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# hostPort

```yaml
containers:
- name: agent
  ports:
  - containerPort: 9100
    hostPort: 9100
    hostIP: 0.0.0.0        # optional; bind to one node IP
    protocol: TCP
```
Traffic to `<nodeIP>:9100` is forwarded to the pod.

## Requirements
- The CNI networking plugin must support `hostPort`. The Kubernetes network plugin documentation
  names the CNI `portmap` plugin (or any plugin with port-mapping capability); to enable it, list
  the `portMappings` capability in the CNI configuration directory. Check your CNI's documentation
  for how it is switched on.
- Pod Security Standards: the Baseline profile requires HostPorts to be disallowed or restricted
  to a known list (undefined or 0 are allowed), so baseline and restricted namespaces can reject
  pods that set `hostPort`.

## Scheduling
The scheduler's NodePorts plugin checks that a node has the requested host ports free. Two pods
wanting the same (hostIP, hostPort, protocol) cannot land on one node; the second stays Pending
with `node(s) didn't have free ports for the requested pod ports`.
Consequences:
- A Deployment with hostPort and more replicas than nodes leaves pods Pending.
- A rolling update that needs a surge pod on a node where the old pod already holds the port
  cannot place the new pod there.

## hostPort vs hostNetwork
| | hostPort | hostNetwork |
|---|---|---|
| pod network namespace | own | the node's |
| ports exposed | only listed | whatever the process binds |

Prefer a Service (NodePort or LoadBalancer) unless the client must reach a specific node, as with
node-local agents.

## Debug
```bash
kubectl describe pod <pod>     # scheduling events: free ports
```
Check on the node that the CNI's port-mapping rules exist; the host process list will not show a
listener for a hostPort, because traffic is forwarded to the pod.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the network plugins page (CNI portmap plugin and portMappings capability), the Pod Security Standards page (Baseline HostPorts control) and the scheduler NodePorts plugin source (exact failure message). Removed claims that specific CNIs ship portmap by default, the iptables chain name, ss/curl commands, the hostNetwork NetworkPolicy comparison and DaemonSet maxSurge statement.

Method: documentation only; no commands were run.
