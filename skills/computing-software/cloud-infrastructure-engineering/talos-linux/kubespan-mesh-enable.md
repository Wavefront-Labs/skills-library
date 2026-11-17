---
id: computing-software.cloud-infrastructure-engineering.talos-linux.kubespan-mesh-enable
name: kubespan-mesh-enable
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [kubespan, kubespanconfig, wireguard, discovery, hybrid-cluster, udp-51820]
level: advanced
status: docs-checked
description: "Enable KubeSpan, Talos automatic WireGuard full mesh: discovery dependency, gen config flag, KubeSpanConfig, UDP 51820 firewall needs and known topology caveats."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/networking/kubespan.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
KubeSpan automates a full mesh WireGuard network so a cluster can span edge, datacenter and cloud. Peer discovery and key exchange go through the cluster discovery service (public at `https://discovery.talos.dev/` by default; a private one needs a commercial licence).

Enable for a new cluster with `talosctl gen config --with-kubespan`, which adds:

```yaml
---
apiVersion: v1alpha1
kind: KubeSpanConfig
enabled: true # Enable the KubeSpan feature.
```

For an existing cluster add the same `KubeSpanConfig` document and make sure discovery is enabled on every machine (it is by default).

Network requirements: all KubeSpan traffic uses UDP port 51820. Best practice is that at least one end of every possible node-to-node path accepts inbound UDP 51820. Workers also need TCP 50000 for initial `talosctl` configuration.

Caveats the page calls out:

- A Kubernetes endpoint IP outside KubeSpan that is forwarded to a control plane node's KubeSpan address (for example a single-node control plane behind a GCP or Azure public IP) makes workers fail to join; put a load balancer in front.
- DigitalOcean anchor IPs can be picked by Flannel as node IP and break pod-to-pod traffic; annotate the node with `flannel.alpha.coreos.com/public-ip-overwrite` and restart the flannel pods.
- Host-port pods must not use 51820.
- Cilium native routing works with KubeSpan (Talos 1.13+) when `advertiseKubernetesNetworks: true` and Cilium sets `bpf.hostLegacyRouting: true`.

## Checked

2026-11-04. Enablement documents, UDP 51820 requirement and the four caveats confirmed on the KubeSpan page.

Method: documentation only; no commands were run.
