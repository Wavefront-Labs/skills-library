---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-airgap-install
name: k3s-airgap-install
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, airgap, install-k3s-skip-download, default-route]
level: advanced
status: docs-checked
description: "Install K3s on air-gapped nodes with a local binary and install.sh, including the default-route and SELinux prerequisites."
sources:
  - https://docs.k3s.io/installation/airgap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: install K3s with no internet access, after the images are loaded (private registry, manual tarball or embedded mirror).

Prerequisites on each node:

- Download the K3s binary matching the airgap images version into /usr/local/bin and `chmod +x` it.
- Download the install script from get.k3s.io and save it as install.sh.
- A default route must exist; K3s needs it to auto-detect the node primary IP and for kube-proxy ClusterIP routing. A black-hole route over a dummy interface is enough:

```
ip link add dummy0 type dummy
ip link set dummy0 up
ip addr add 203.0.113.254/31 dev dummy0
ip route add default via 203.0.113.255 dev dummy0 metric 1000
```

- With SELinux enabled, manually install the k3s-selinux RPM first. It depends on container-selinux, policycoreutils and selinux-policy.

Single server:

```
INSTALL_K3S_SKIP_DOWNLOAD=true ./install.sh
```

Agents:

```
INSTALL_K3S_SKIP_DOWNLOAD=true K3S_URL=https://<SERVER_IP>:6443 K3S_TOKEN=<YOUR_TOKEN> ./install.sh
```

For HA, keep INSTALL_K3S_SKIP_DOWNLOAD=true, run the script locally, and pass arguments with INSTALL_K3S_EXEC, for example `INSTALL_K3S_EXEC='server --token=SECRET' K3S_DATASTORE_ENDPOINT='mysql://username:password@tcp(hostname:3306)/database-name' ./install.sh`.

The --resolv-conf flag is passed to the kubelet and can help pod DNS where the host has no upstream nameservers.

## Checked

2026-11-03: read docs.k3s.io installation/airgap. Confirmed: the default-route requirement and the dummy0 route commands, the k3s-selinux dependencies (container-selinux, policycoreutils, selinux-policy), INSTALL_K3S_SKIP_DOWNLOAD usage for single server, agents and HA, and the --resolv-conf note.

Method: documentation only; no commands were run.
