---
id: computing-software.cloud-infrastructure-engineering.talos-linux.cilium-cni-on-talos
name: cilium-cni-on-talos
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [cilium, cni, kube-proxy-free, helm, kubeprism, inline-manifest, kubeflannelcniconfig, gateway-api]
level: practitioner
status: docs-checked
description: "Install Cilium on Talos: disable Flannel and optionally kube-proxy first, Helm values that fit Talos (capabilities, cgroup, KubePrism 7445), inline manifest, known issues."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/kubernetes-guides/cni/deploying-cilium.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos requirements for Cilium: IPAM mode `kubernetes`; do not let Cilium mount `cgroupv2` or `bpffs` (Talos already does); drop `SYS_MODULE` because workloads cannot load kernel modules; the guide assumes KubePrism on port `7445`.

Before bootstrap, remove Flannel (Talos v1.14 and later). For kube-proxy-free operation, also disable kube-proxy:

```bash
cat <<'EOF' > patch.yaml
apiVersion: v1alpha1
kind: KubeFlannelCNIConfig
$patch: delete
---
apiVersion: v1alpha1
kind: KubeProxyConfig
enabled: false
EOF
```

```bash
talosctl gen config \
    <cluster-name> https://<cluster-endpoint>:6443 \
    --config-patch-control-plane @patch.yaml
```

Older than v1.14 uses `cluster.network.cni.name: none` (and `cluster.proxy.disabled: true`). After bootstrap Talos waits at phase 18/19 with `retrying error: node not ready`; you have about 10 minutes to install Cilium.

Helm install, kube-proxy-free variant:

```bash
helm install \
    cilium \
    cilium/cilium \
    --version 1.18.0 \
    --namespace kube-system \
    --set ipam.mode=kubernetes \
    --set kubeProxyReplacement=true \
    --set securityContext.capabilities.ciliumAgent="{CHOWN,KILL,NET_ADMIN,NET_RAW,IPC_LOCK,SYS_ADMIN,SYS_RESOURCE,DAC_OVERRIDE,FOWNER,SETGID,SETUID}" \
    --set securityContext.capabilities.cleanCiliumState="{NET_ADMIN,SYS_ADMIN,SYS_RESOURCE}" \
    --set cgroup.autoMount.enabled=false \
    --set cgroup.hostRoot=/sys/fs/cgroup \
    --set k8sServiceHost=localhost \
    --set k8sServicePort=7445
```

With kube-proxy, set `kubeProxyReplacement=false` and omit the last two flags. Production-preferred: render with `helm template` and embed it in control plane machine configs as a `KubeInlineManifestConfig` (`name: cilium`, `manifest: |`); Talos only creates missing resources, so to update edit all control plane configs and run `talosctl upgrade-k8s`. A hosted manifest uses `cni.name: custom` with `urls`, but the manifest holds key material, so host it privately.

Known issues: with `forwardKubeDNSToHost=true` plus `bpf.masquerade=true`, CoreDNS may fail (set `forwardKubeDNSToHost=false`); `cilium connectivity test` trips Pod Security on `NET_RAW`, so label its namespace `pod-security.kubernetes.io/enforce=privileged`.

## Checked

2026-11-04. Prerequisites, patches, Helm flags, inline manifest rules and known issues confirmed on the Deploy Cilium CNI page.

Method: documentation only; no commands were run.
