---
id: computing-software.cloud-infrastructure-engineering.kubespray.offline-inventory-overrides
name: offline-inventory-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [offline, air-gapped, files-repo, registry-host, kube-image-repo, mirror]
level: advanced
status: docs-checked
description: "Point Kubespray at internal mirrors with registry_host, registry_addr, files_repo and the image repo and download URL overrides from the sample offline.yml."
sources:
  - https://kubespray.io/docs/operations/offline-environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
After the artifacts are reachable, adjust these variables in the inventory (the sample is `inventory/sample/group_vars/all/offline.yml`):

```yaml
kube_image_repo: "{{ registry_host }}"
gcr_image_repo: "{{ registry_host }}"
docker_image_repo: "{{ registry_host }}"
quay_image_repo: "{{ registry_host }}"
github_image_repo: "{{ registry_host }}"
github_url: "{{ files_repo }}/github.com"
dl_k8s_io_url: "{{ files_repo }}/dl.k8s.io"
storage_googleapis_url: "{{ files_repo }}/storage.googleapis.com"
get_helm_url: "{{ files_repo }}/get.helm.sh"
local_path_provisioner_helper_image_repo: "{{ registry_host }}/busybox"
```

Then define the variables those lines use:
- `registry_host`: the container image registry. If you keep the same repository paths as the defaults in kubespray-defaults, no further `*_image_repo` overrides are needed; otherwise override each.
- `registry_addr`: the registry as `[domain or ip]:[port]` only.
- `files_repo`: an HTTP server or proxy serving the files. The path is not important; the page recommends `*_version` in the path so it need not change on each upgrade.
- `yum_repo`, `debian_repo`, `ubuntu_repo`: OS repositories, used only for Docker/Containerd packages; other packages may come from other repos, which you can stop by skipping the `system-packages` tag.

For OS-specific Docker repo settings, define only the one matching your OS.

## Checked

The variable block and the variable descriptions were confirmed in the Configure Inventory section of the Offline environment page; the OS-specific repository variables were not reproduced.

Method: docs-checked 2026-11-09 against the Kubespray docs/operations/offline-environment.md page (full file read).
