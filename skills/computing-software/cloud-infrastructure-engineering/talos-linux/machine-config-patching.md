---
id: computing-software.cloud-infrastructure-engineering.talos-linux.machine-config-patching
name: machine-config-patching
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [machine-config, patching, strategic-merge, patch-delete, gen-config, multi-document, talosctl-patch]
level: practitioner
status: docs-checked
description: "Strategic merge patches for Talos machine config: merge and list-append rules, replaced fields, deleting fields or documents with $patch: delete, and the talosctl patch flags."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/patching.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Patches look like incomplete machine configs and may be multi-document (`---`). Patch values override base values. Rules: lists are appended, except `KubeNetworkConfig.podSubnets` and `serviceSubnets` (overwritten), `network.interfaces` (merged on `interface:` or `deviceSelector:`), `network.interfaces.vlans` (on `vlanId:`) and `ExtensionServiceConfig.configFiles` (on `mountPath`). Replaced wholesale: `KubeAuditPolicyConfig.configuration`, `KubeAuthenticationConfig.configuration`, `KubeCredentialProviderConfig.configuration`, `KubeStaticPodConfig.pod`. Named documents match on `kind`, `apiVersion` and `name`; a missing document is appended. One patch file cannot modify the same document twice.

Delete a field, or a document (not the main `v1alpha1` one):

```yaml
apiVersion: v1alpha1
kind: LinkConfig
name: enp0s3
mtu:
  $patch: delete
---
apiVersion: v1alpha1
kind: SideroLinkConfig
$patch: delete
```

Example: update subnets and drop the default CNI by deleting the Flannel document:

```yaml
apiVersion: v1alpha1
kind: KubeNetworkConfig
podSubnets:
  - 192.168.0.0/16
serviceSubnets:
  - 192.0.0.0/12
---
apiVersion: v1alpha1
kind: KubeFlannelCNIConfig
$patch: delete
```

CLI usage (inline or `@file`; applied in order; JSON patch or strategic merge auto-detected):

```shell
talosctl gen config test-cluster https://172.20.0.1:6443 \
  --config-patch @all.yaml \
  --config-patch-control-plane cp.yaml \
  --config-patch-worker worker.yaml
talosctl machineconfig patch worker.yaml --patch patch.yaml -o worker1.yaml
talosctl patch mc --nodes 172.20.0.2 --patch patch.yaml
```

Multi-document patches can be applied in maintenance mode with `talosctl apply -f <machine-configuration> --insecure --node <node-ip> --patch <multi-document>`.

## Checked

2026-11-04. Patching page confirms the merge rules, delete syntax, the Flannel example and the three CLI patch routes.

Method: documentation only; no commands were run.
