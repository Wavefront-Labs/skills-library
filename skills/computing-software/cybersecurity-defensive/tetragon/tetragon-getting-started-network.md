---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-getting-started-network
name: tetragon-getting-started-network
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [demo-network, tetragon, tcp-connect, egress-monitoring]
level: intro
status: docs-checked
description: "Monitor TCP connections leaving a Kubernetes cluster or Docker host with the Tetragon network_egress_cluster quickstart policy."
sources:
  - "https://tetragon.io/docs/getting-started/network/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor network access with Tetragon

Goal: report connections to "external" destinations, outside the Kubernetes cluster or the Docker host, while in-kernel BPF filters suppress internal traffic.

## Kubernetes

Find the CIDRs:

```shell
export PODCIDR=`kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}'`
```

`SERVICECIDR` comes from per-platform commands (GKE, Kind, EKS, AKS) listed on the page. Then substitute and apply:

```shell
wget https://raw.githubusercontent.com/cilium/tetragon/main/examples/quickstart/network_egress_cluster.yaml
envsubst < network_egress_cluster.yaml | kubectl apply -f -
```

The policy `monitor-network-activity-outside-cluster-cidr-range` is a kprobe on `tcp_connect` (`syscall: false`, arg 0 type `sock`) with a `matchArgs` operator `NotDAddr` over `127.0.0.1`, `${PODCIDR}` and `${SERVICECIDR}`.

Observe, then trigger a connection:

```shell
kubectl exec -ti -n kube-system ds/tetragon -c tetragon -- tetra getevents -o compact --pods xwing --processes curl
kubectl exec -ti xwing -- bash -c 'curl https://ebpf.io/applications/#tetragon'
```

```
🚀 process default/xwing /usr/bin/curl https://ebpf.io/applications/#tetragon
🔌 connect default/xwing /usr/bin/curl tcp 10.32.0.19:33978 -> 104.198.14.52:443
💥 exit    default/xwing /usr/bin/curl https://ebpf.io/applications/#tetragon 60
```

A curl to `deathstar.default.svc.cluster.local` gives no `connect` event, only process and exit. Delete with `envsubst < network_egress_cluster.yaml | kubectl delete -f -`.

## Docker or bare metal

No pod or service CIDR exists, so set both to loopback, render the policy to a file, and mount it into the container at `/etc/tetragon/tetragon.tp.d/`:

```shell
export PODCIDR="127.0.0.1/32"
export SERVICECIDR="127.0.0.1/32"
envsubst < network_egress_cluster.yaml > network_egress_cluster_subst.yaml
```

Then run `docker exec -ti tetragon tetra getevents -o compact`. Remote TCP connects are logged and localhost ones are filtered out.

## Checked

Date: 2026-11-07

Network getting-started page read in full, plus the network_egress_cluster.yaml quickstart policy.

Method: documentation only; no commands were run.
