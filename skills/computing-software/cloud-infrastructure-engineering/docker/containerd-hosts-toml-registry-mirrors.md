---
id: computing-software.cloud-infrastructure-engineering.docker.containerd-hosts-toml-registry-mirrors
name: containerd-hosts-toml-registry-mirrors
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, containerd, registry-mirror, containerd-mirror, hosts-toml, kubernetes-nodes, insecure-registries]
level: advanced
description: "Configure containerd registry mirrors, private CAs and insecure registries per host with certs.d/<host>/hosts.toml for Kubernetes nodes and nerdctl."
sources: ["https://github.com/containerd/containerd/blob/main/docs/hosts.md", "https://github.com/containerd/containerd/blob/main/docs/cri/registry.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# containerd hosts.toml mirrors

Kubernetes nodes run containerd, not dockerd: `daemon.json` mirrors do nothing there.

## Enable the config path (containerd 1.x CRI)
```toml
# /etc/containerd/config.toml
version = 2
[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"
```
containerd 2.x uses `version = 3` and `[plugins."io.containerd.cri.v1.images".registry]`.
The legacy CRI `registry.mirrors` / `registry.configs` pattern is deprecated; use `config_path`. Restart
containerd once for the config.toml change; updates under the certs directory do not require restarting containerd.

## Mirror Docker Hub
```toml
# /etc/containerd/certs.d/docker.io/hosts.toml
server = "https://registry-1.docker.io"

[host."https://mirror.example.com"]
  capabilities = ["pull", "resolve"]
  ca = "/etc/containerd/certs.d/docker.io/mirror-ca.crt"
```
Hosts are tried first in the order listed, then `server` is used as the fallback.

## Path-prefixed caches (Harbor proxy project, ECR pull-through)
```toml
# /etc/containerd/certs.d/docker.io/hosts.toml
server = "https://registry-1.docker.io"
[host."https://harbor.example.com/v2/dockerhub-proxy"]
  capabilities = ["pull", "resolve"]
  override_path = true
```
`override_path = true` indicates the host's API root endpoint is defined in the URL path rather than by the
API specification (default `false`). When a host differs from the registry host namespace, containerd also
adds the namespace as an `ns` query parameter.

## Private registry with own CA / insecure
```toml
# /etc/containerd/certs.d/registry.lab:5000/hosts.toml
server = "https://registry.lab:5000"
[host."https://registry.lab:5000"]
  ca = "/etc/containerd/certs.d/registry.lab:5000/ca.crt"
  # skip_verify = true          # lab only
[host."http://registry.lab:5000"]  # plain HTTP
```
The directory name is the registry host namespace: the host name or IP address with an optional port.
`_default` can be used as a fallback namespace when no other namespace matches.

## Gotchas
- Resolving (name to digest) must be a trusted operation and a public mirror should never be trusted to
  resolve: give a public mirror `capabilities = ["pull"]`; a private mirror may also resolve. Push belongs on
  the upstream source only.

## Verify
```sh
crictl pull docker.io/library/alpine:3.20
journalctl -u containerd | grep -i 'mirror.example.com'
```

## Checked

2026-10-26. Documentation release: containerd/containerd docs/hosts.md at main (repository pushed 2026-10-23). Confirmed: config_path for containerd 2.x (version 3, io.containerd.cri.v1.images) and 1.x (version 2, io.containerd.grpc.v1.cri), deprecation of the old CRI mirrors pattern, no restart needed for certs.d updates, server/host ordering and fallback, capabilities semantics and the trust table, ca and skip_verify fields, plain http host entries, override_path meaning and default, _default namespace, ns query parameter, namespace directory naming with port. Removed unconfirmed claims: mixing legacy and config_path being an error, managed node image behaviour, kubelet pull secret matching, and the nerdctl debug command.

Method: documentation only; no commands were run.
