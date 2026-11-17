---
id: computing-software.cloud-infrastructure-engineering.kubespray.docker-container-manager-options
name: docker-container-manager-options
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [docker, container-manager, cri-dockerd, overlay2, cgroup-driver, insecure-registries]
level: practitioner
status: docs-checked
description: "Use container_manager docker through cri-dockerd and tune docker_cgroup_driver, docker_storage_options, docker_log_opts, registry mirrors, DNS strictness and daemon options."
sources:
  - https://kubespray.io/docs/CRI/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docker is supported by Kubespray. Because dockershim is deprecated and slated for removal in Kubernetes 1.24+, `cri-dockerd` (Mirantis) is the alternative, and it replaced dockershim across supported Kubernetes versions in Kubespray 2.20.

```yaml
container_manager: docker
```

Documented options:
- `docker_storage_options: -s overlay2` enables overlay2.
- `docker_cgroup_driver` is `systemd` (default) or `cgroupfs`.
- `docker_dns_servers_strict: false` stops the deployment failing when you have more than 3 nameservers (Kubespray uses the first 3 or fails).
- `docker_daemon_graph` sets the data path (`/var/lib/docker`).
- `docker_iptables_enabled: "false"` changes daemon iptables support.
- Log rotation: `docker_log_opts: "--log-opt max-size=50m --log-opt max-file=5"`.
- `docker_bin_dir` should only change for a custom docker package.
- `docker_rpm_keepcache: 1` keeps packages, since Kubespray deletes the docker package on each run.
- `docker_insecure_registries` (IPs or domain names) and `docker_registry_mirrors`.
- `docker_mount_flags` takes `shared`, `slave` or `private`; empty is the system default.
- `docker_options` passes extra daemon options verbatim.
- `docker_repo_key_keyring` sets the GPG key path on Debian-based systems to avoid the default `apt_key` location.

The Upgrades page notes that migrating container engines is not officially supported by Kubespray.

## Checked

2026-11-04. Every option was confirmed on the Docker support page; the closing remark is from the Upgrades page.

Method: documentation only; no commands were run.
