---
id: computing-software.cloud-infrastructure-engineering.kubespray.multus-secondary-networks
name: multus-secondary-networks
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [multus, cni, network-attachment-definition, macvlan, cilium, namespace-isolation]
level: advanced
status: docs-checked
description: "Install Multus beside a primary CNI in Kubespray, enable namespace isolation, set cilium_cni_exclusive false and attach extra interfaces."
sources:
  - https://kubespray.io/docs/CNI/multus.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Multus is a meta CNI plugin giving pods multiple interfaces; it delegates to secondary CNI plugins. Because it implements no networking itself, it needs a primary plugin in `kube_network_plugin`, plus the Multus switch:

```yml
kube_network_plugin: calico
kube_network_plugin_multus: true
```

Namespace isolation, where pods may only use `NetworkAttachmentDefinitions` in their own namespace:

```yml
multus_namespace_isolation: true
```

With Cilium as primary, set `cilium_cni_exclusive` to `false` so Cilium does not revert the Multus config:

```yml
kube_network_plugin: cilium
kube_network_plugin_multus: true
cilium_cni_exclusive: false
```

**Using it.** Create a `NetworkAttachmentDefinition` (apiVersion `k8s.cni.cncf.io/v1`) whose `spec.config` holds any valid CNI configuration whose binary exists on the nodes; the page uses a `macvlan` config named `macvlan-conf` with `host-local` IPAM on 192.168.1.0/24. Then reference it from a pod with the annotation:

```yaml
metadata:
  annotations:
    k8s.v1.cni.cncf.io/networks: macvlan-conf
```

Inspect with `kubectl exec -it samplepod -- ip a` to see the extra interface.

## Checked

2026-11-08. Cited pages re-read in full. The variables, Cilium compatibility and annotation usage were confirmed on the Multus page; only the key fragment of the attachment definition is reproduced.

Method: documentation only; no commands were run.
