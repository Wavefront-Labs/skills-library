---
id: computing-software.cloud-infrastructure-engineering.linkerd.cni-plugin-install
name: cni-plugin-install
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, cni, iptables, install, net-admin]
level: advanced
status: docs-checked
description: "Replace the linkerd-init container with the Linkerd CNI plugin when pods cannot hold CAP_NET_ADMIN, installing the DaemonSet first."
sources:
  - https://linkerd.io/2.19/features/cni/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default an init container uses iptables to redirect pod traffic to the proxy, which needs `CAP_NET_ADMIN`. Where that capability is not granted, run the iptables rules in Linkerd's CNI plugin instead. It works by CNI chaining alongside your existing CNI plugin, handling only Linkerd-specific configuration.

The `linkerd-cni` DaemonSet must be installed before the control plane:

```bash
linkerd install-cni | kubectl apply -f -
linkerd install --linkerd-cni-enabled | kubectl apply -f -
```

`--linkerd-cni-enabled` sets `cniEnabled` in the `linkerd-config` ConfigMap, and proxy injection then omits the `linkerd-init` container.

With Helm, install the CNI chart first, then add `--set cniEnabled=true` to both the `linkerd-crds` and `linkerd-control-plane` installs.

If you run Cilium, install it with `cni.exclusive=false` so that Cilium does not take ownership of the CNI configuration directory and other plugins can deploy their configuration there.

After the DaemonSet is running, meshed pods should no longer use the `linkerd-init` init container, which is a quick way to confirm that the plugin is active: list a new pod's init containers and check that it is absent.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/features/cni/.

Removed or reworded: Nothing.

Method: documentation only; no commands were run.
