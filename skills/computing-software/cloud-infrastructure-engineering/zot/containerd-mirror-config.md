---
id: computing-software.cloud-infrastructure-engineering.zot.containerd-mirror-config
name: containerd-mirror-config
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, containerd, registry-mirror, hosts-toml, config-path, cri-plugin]
level: practitioner
status: docs-checked
description: "Point containerd v1.x and v2.x at Zot as a registry mirror, including the required /v2 path segment and the certs.d hosts.toml layout."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/containerd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
containerd supports registry mirroring and Zot can be the upstream. The example mirrors a Zot repository named `docker` for Docker Hub (`docker.io`) pulls.

containerd v1.x:

```
version = 2

[plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
endpoint = ['https://<my zot instance>:8080/v2/docker']
```

The `/v2` path segment is required.

containerd v2.x:

```
version = 3

[plugins."io.containerd.cri.v1.images".registry]
  config_path = "/etc/containerd/certs.d"
```

Then lay out `/etc/containerd/certs.d/_default/hosts.toml`:

```
# zot is running at localhost:8080
server = "http://localhost:8080"
```

For other mirror options see containerd's `hosts.md` documentation.

## Checked

Config examples confirmed. Dropped an unsourced related-config remark.

Method: docs-checked 2026-11-09 against zot docs articles/containerd.md (read in full).
