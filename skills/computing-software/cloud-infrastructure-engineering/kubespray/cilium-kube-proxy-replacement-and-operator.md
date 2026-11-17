---
id: computing-software.cloud-infrastructure-engineering.kubespray.cilium-kube-proxy-replacement-and-operator
name: cilium-kube-proxy-replacement-and-operator
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [cilium, kube-proxy-replacement, operator, custom-args, extra-volumes, version]
level: advanced
status: docs-checked
description: "Run Cilium without kube-proxy in Kubespray, pin cilium_version, add config keys, and set Operator custom args and extra volumes."
sources:
  - https://kubespray.io/docs/CNI/cilium.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Kube-proxy replacement.** Set `cilium_kube_proxy_replacement` to `strict` (before Cilium v1.16) or `true`. Cilium 1.16+ no longer accepts `strict`; Kubespray converts it to `true` for those versions. Without kube-proxy, Cilium must know the kube-apiserver address, set globally for agents and operators. The localhost apiserver load balancer can be used only when it uses the same port as kube-apiserver (the default).

**Operator.** The Cilium Operator does not exist for installation; it handles duties that logically happen once per cluster rather than per node.

Extra container arguments (advanced; array or string):

```yml
cilium_operator_custom_args: ["--foo=bar", "--baz=qux"]
```

Do not add a flag to enable debugging; use the `CILIUM_DEBUG` variable.

Extra volumes:

```yml
cilium_operator_extra_volumes:
  - configMap:
      name: foo
    name: foo-mount-path

cilium_operator_extra_volume_mounts:
  - mountPath: /tmp/foo/bar
    name: foo-mount-path
    readOnly: true
```

**Version and config.**

```yml
cilium_version: "1.20.4"
cilium_config_extra_vars:
  enable-endpoint-routes: true
```

**Identity allocation mode.** `crd` stores identities as CRDs (query `kubectl get ciliumid`); `kvstore` stores them in etcd, where Kubespray renders the Helm etcd values from `etcd_access_addresses` and creates the `cilium-etcd-secrets` Secret from the first control plane node's etcd client certificate, working with every `etcd_deployment_type`.

## Checked

2026-11-08. Cited pages re-read in full. Kube-proxy replacement values, operator options, version, extra vars and identity modes were confirmed on the Cilium page.

Method: documentation only; no commands were run.
