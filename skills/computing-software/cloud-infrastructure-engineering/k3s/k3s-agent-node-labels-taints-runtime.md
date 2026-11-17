---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-agent-node-labels-taints-runtime
name: k3s-agent-node-labels-taints-runtime
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, node-label, node-taint, container-runtime-endpoint]
level: practitioner
status: docs-checked
description: "Set node labels and taints at registration and use agent flags for runtime, networking and node identity."
sources:
  - https://docs.k3s.io/cli/agent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Labels and taints:

```
--node-label foo=bar \
--node-label hello=world \
--node-taint key1=value1:NoExecute
```

These apply only at registration time, so they are set once and cannot be changed again by K3s commands. Use kubectl to change labels and taints later.

Node identity: `--node-name` ($K3S_NODE_NAME), `--with-node-id` (append an id), `--node-ip`/`-i`, `--node-external-ip`, `--node-internal-dns`, `--node-external-dns`, `--resolv-conf` ($K3S_RESOLV_CONF).

Runtime:

- --container-runtime-endpoint: disable embedded containerd and use the CRI socket at that path (with --docker it sets the docker socket)
- --image-service-endpoint: disable the embedded image service and use a remote one
- --default-runtime: containerd default runtime
- --pause-image (default rancher/mirrored-pause:3.6)
- --snapshotter (default overlayfs)
- --private-registry (default /etc/rancher/k3s/registries.yaml)
- --disable-default-registry-endpoint
- --nonroot-devices

Other: --selinux ($K3S_SELINUX), --protect-kernel-defaults (error if kernel tunables differ from kubelet defaults), --lb-server-port ($K3S_LB_SERVER_PORT, default 6444), --disable-apiserver-lb (experimental: skip the agent client-side load balancer and connect directly to the configured server), --data-dir ($K3S_DATA_DIR), --token/-t, --token-file, --server/-s.

Because labels and taints are only read at registration, an agent that has already joined ignores changed values in its service file or config; change them with kubectl instead. Flags can equally be written as keys in the config file, for example `node-label:` as a list.

## Checked

2026-11-03: read docs.k3s.io cli/agent. Confirmed: the --node-label/--node-taint registration-time behaviour, node identity flags, the runtime flags and their defaults, --lb-server-port 6444 and --disable-apiserver-lb.

Method: documentation only; no commands were run.
