---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-runtime-hooks-install
name: tetragon-runtime-hooks-install
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [runtime-hooks-install]
level: advanced
status: docs-checked
description: "Install Tetragon with runtime hooks on minikube or kind using CRI-O OCI hooks or containerd NRI, then test that the hook reaches the agent."
sources:
  - "https://tetragon.io/docs/installation/runtime-hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install Tetragon with runtime hooks

Goal: enable the `tetragon-rthooks` daemonset so container creation is reported to the agent. The guide uses minikube (supports both `cri-o` and `containerd`); the steps apply to other platforms.

## Set up the cluster

```shell
minikube start --driver=kvm2 --container-runtime=cri-o
minikube start --driver=kvm2 --container-runtime=containerd
```

Hooks on containerd use NRI, enabled by default from containerd 2.0. For 1.7 it must be enabled with this containerd config section (for example `/etc/containerd/config.toml`):

```toml
[plugins."io.containerd.nri.v1.nri"]
  disable = false
  disable_connections = false
  plugin_config_path = "/etc/nri/conf.d"
  plugin_path = "/opt/nri/plugins"
  plugin_registration_timeout = "5s"
  plugin_request_timeout = "2s"
  socket_path = "/var/run/nri/nri.sock"
```

`./contrib/tetragon-rthooks/scripts/minikube-install-hook.sh --nri` patches the file and restarts containerd. For kind (containerd only), create the cluster with the `/procHost` mount and `--set tetragon.hostProcPath=/procHost`, check the version with `docker exec -it kind-control-plane crictl version`, and if earlier than 2.0 run `./contrib/tetragon-rthooks/scripts/kind-hook-setup.sh`.

## Install

```shell
helm repo add cilium https://helm.cilium.io
helm repo update
helm install --namespace kube-system --set rthooks.enabled=true --set rthooks.interface=oci-hooks tetragon cilium/tetragon
```

Use `--set rthooks.interface=nri-hook` for containerd. Add `${EXTRA_HELM_FLAGS[@]}` for kind. Check `kubectl -n kube-system get pods | grep tetragon` shows tetragon, tetragon-operator and tetragon-rthooks pods running.

## Test

Start a pod with `kubectl run test --image=debian --rm -it -- /bin/bash`, then read the hook log:

```shell
minikube ssh 'tail -1 /opt/tetragon/tetragon-oci-hook.log'
docker exec kind-control-plane sh -c 'tail -1 /opt/tetragon/tetragon-oci-hook.log'
```

Expect an INFO line with `"msg":"hook request to agent succeeded"` and `"hook":"create-container"`.

## Checked

2026-11-08. Read the runtime hooks installation page in full (raw docs markdown). Checked cluster setup, NRI configuration, helm install and test steps against it; no claims removed.

Method: documentation only; no commands were run.
