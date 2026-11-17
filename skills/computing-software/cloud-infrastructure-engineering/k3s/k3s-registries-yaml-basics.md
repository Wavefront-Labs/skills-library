---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-registries-yaml-basics
name: k3s-registries-yaml-basics
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, registries-yaml, mirrors, configs]
level: practitioner
status: docs-checked
description: "Configure containerd registry mirrors, authentication and TLS for K3s in /etc/rancher/k3s/registries.yaml."
sources:
  - https://docs.k3s.io/installation/private-registry
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pull from private or mirrored registries.

At startup K3s checks /etc/rancher/k3s/registries.yaml and uses it to generate the containerd configuration. Create it on every node that pulls from the registry, including servers that run workloads (servers are schedulable by default). Restart K3s on each node for changes to take effect.

Structure:

```
mirrors:
  <REGISTRY>:
    endpoint:
      - https://<REGISTRY>/v2
configs:
  <REGISTRY>:
    auth:
      username: <BASIC AUTH USERNAME>
      password: <BASIC AUTH PASSWORD>
      auth: <BASE64 USERNAME:PASSWORD>
    tls:
      ca_file: <PATH TO SERVER CA>
      cert_file: <PATH TO CLIENT CERT>
      key_file: <PATH TO CLIENT KEY>
      insecure_skip_verify: <BOOLEAN>
```

containerd tries the listed endpoints plus the default endpoint and uses the first that works. Auth is either username/password or the base64 auth token. Without TLS you must write `http://` in the endpoint, otherwise https is assumed:

```
mirrors:
  docker.io:
    endpoint:
      - "http://registry.example.com:5000"
```

Docker Hub with credentials uses endpoint `https://index.docker.io/v2` and a configs entry of the same URL with username and password (or a personal access token).

## Checked

2026-11-08. Read the full K3s Private Registry Configuration page (docs/installation/private-registry.md in the k3s-io/docs repo). Confirmed: startup check of registries.yaml, per-node and server-node placement, restart requirement, the mirrors and configs structure with auth and tls keys, default endpoint trial order, http:// without TLS, and the Docker Hub credentials example. Nothing removed.

Method: documentation only; no commands were run.
