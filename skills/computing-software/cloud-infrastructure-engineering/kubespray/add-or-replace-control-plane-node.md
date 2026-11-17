---
id: computing-software.cloud-infrastructure-engineering.kubespray.add-or-replace-control-plane-node
name: add-or-replace-control-plane-node
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [scale, control-plane, cluster-yml, nginx-proxy, remove-node]
level: advanced
status: docs-checked
description: "Add a control plane node by appending to kube_control_plane and running cluster.yml (not scale.yml), restart nginx-proxy everywhere, then remove the old node."
sources:
  - https://kubespray.io/docs/operations/nodes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Control plane nodes cannot be added with `scale.yml`.

1. Append the new host to the inventory and run `cluster.yml`. Always append it to the end of the `kube_control_plane` group; adding in the first position is not supported and makes the playbook fail.
2. Restart the `nginx-proxy` pod in `kube-system` on all hosts. It is the local proxy for the apiserver; Kubespray updates its static config but the pod must restart to reload. The page gives:

```sh
# run in every host
docker ps | grep k8s_nginx-proxy_nginx-proxy | awk '{print $1}' | xargs docker restart

# or with containerd
crictl ps | grep nginx-proxy | awk '{print $1}' | xargs crictl stop
```

3. With the old node still in the inventory, run `remove-node.yml -e node=NODE_NAME`. If it is offline, pass:

```
-e '{"reset_nodes": false, "allow_ungraceful_removal": true}'
```

## Checked

2026-11-04. Steps, commands and the ordering warning were confirmed on the Adding/replacing a node page, control plane section. An unsupported closing remark was removed.

Method: documentation only; no commands were run.
