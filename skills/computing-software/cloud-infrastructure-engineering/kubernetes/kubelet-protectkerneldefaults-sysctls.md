---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-protectkerneldefaults-sysctls
name: kubelet-protectkerneldefaults-sysctls
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, node-kubelet-hardening, protectkerneldefaults, kubelet, sysctls, cis-benchmark]
level: practitioner
status: docs-checked
description: "Enable kubelet protectKernelDefaults safely by setting the kernel sysctls it expects first, so hardened nodes start instead of crash-looping the kubelet."
sources: ["https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/cm/container_manager_linux.go", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/component-helpers/node/util/sysctl/sysctl.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# protectKernelDefaults

With `protectKernelDefaults: true`, the kubelet refuses to start if kernel tunables differ from
the values it wants, instead of changing them itself. Turning it on
without preparing the node makes the kubelet exit:
```
Failed to start ContainerManager [invalid kernel flag: vm/overcommit_memory, expected value: 1, actual value: 0, ...]
```

## Set the sysctls first
```bash
cat <<'EOF' | sudo tee /etc/sysctl.d/90-kubelet.conf
vm.overcommit_memory = 1
vm.panic_on_oom = 0
kernel.panic = 10
kernel.panic_on_oops = 1
kernel.keys.root_maxkeys = 1000000
kernel.keys.root_maxbytes = 25000000
EOF
sudo sysctl --system
```

## Then enable
```yaml
# /var/lib/kubelet/config.yaml
protectKernelDefaults: true
```
`sudo systemctl restart kubelet` and watch `journalctl -u kubelet -f`.

## Roll out
- Put the sysctl file into the node image or config management before changing the kubelet
  config fleet-wide.
- On kubeadm, update the `kubelet-config` ConfigMap so joining nodes get the setting, and
  `kubeadm upgrade node phase kubelet-config` on existing nodes.
- The expected list is hard-coded in the kubelet (`setupKernelTunables`); read kubelet errors after upgrades.
- Without the option the kubelet modifies these sysctls itself to match.

## Verify
```bash
sysctl vm.overcommit_memory kernel.panic kernel.panic_on_oops
kubectl get --raw /api/v1/nodes/<node>/proxy/configz | jq .kubeletconfig.protectKernelDefaults
```
Node stays Ready after a reboot.

## Checked

2026-10-26: kubelet config API source and container manager source (kubernetes/kubernetes main, 2026-10-25). Confirmed: protectKernelDefaults default false, error-versus-modify behaviour, the exact list of six tunables and values (vm.overcommit_memory 1, vm.panic_on_oom 0, kernel.panic 10, kernel.panic_on_oops 1, kernel.keys.root_maxkeys 1000000, kernel.keys.root_maxbytes 25000000) and the error message format. kubeadm kubelet-config phase confirmed in the kubeadm upgrade reference.

Method: documentation only; no commands were run.
