---
id: computing-software.cloud-infrastructure-engineering.talos-linux.discovery-service-registries
name: discovery-service-registries
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [discovery, cluster-membership, discoveryserviceconfig, affiliates, kubespan, kubeprism, registry, encryption]
level: advanced
status: docs-checked
description: "Talos cluster discovery: encrypted service registry, DiscoveryServiceConfig (self-hosted, HA), deprecated Kubernetes registry, outage behaviour, inspecting members."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/discovery.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Discovery lets nodes learn each other's addresses and is required by KubeSpan and KubePrism. The **service registry** (default) talks to `https://discovery.talos.dev/` on TCP 443; affiliate data is encrypted by nodes (AES-GCM; endpoints separately with AES in ECB mode for server-side dedup), so the service never sees the key. The cluster ID from the cluster secrets separates clusters. The **Kubernetes registry** (node annotations) is deprecated and off by default because the Kubernetes 1.32 `AuthorizeNodeWithSelectors` gate breaks it.

A generated config contains:

```yaml
apiVersion: v1alpha1
kind: DiscoveryServiceConfig
name: default
endpoint: https://discovery.talos.dev/
```

Self-hosted or HA: add documents with unique names; endpoints use `http://`, `https://` or `grpc://`, nodes publish to all of them.

```yaml
apiVersion: v1alpha1
kind: DiscoveryServiceConfig
name: discovery-1
endpoint: https://discovery-1.example.com/
---
apiVersion: v1alpha1
kind: DiscoveryServiceConfig
name: discovery-2
endpoint: https://discovery-2.example.com/
```

Remove all such documents to disable discovery (KubeSpan and KubePrism then stop working correctly, bootstrap and recovery get slower). These documents and the legacy `.cluster.discovery` block are mutually exclusive.

**Outages.** Records have a hardcoded 30 minute TTL. Short outages use cached state; a rebooted node cannot publish or fetch until the service returns; beyond the TTL the service may return an empty set and KubeSpan may blip before self-recovering. With KubeSpan, WireGuard keys regenerate each boot.

Inspect: `talosctl get identities -o yaml`, `talosctl get affiliates`, `talosctl get affiliates --namespace=cluster-raw` (prefixes `k8s/` or `service/`), `talosctl get members`.

## Checked

2026-11-04. Discovery Service page confirms registries, the YAML documents, the legacy block exclusivity, TTL and outage behaviour, and the inspection commands.

Method: documentation only; no commands were run.
