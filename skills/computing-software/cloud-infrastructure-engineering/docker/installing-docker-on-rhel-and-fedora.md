---
id: computing-software.cloud-infrastructure-engineering.docker.installing-docker-on-rhel-and-fedora
name: installing-docker-on-rhel-and-fedora
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, engine-install, dnf-install, rhel-docker, fedora, podman-conflict, selinux]
level: practitioner
status: docs-checked
description: "Install Docker Engine on RHEL, Rocky/Alma, CentOS Stream or Fedora: removing podman-docker/buildah conflicts, adding the docker-ce repo with dnf, SELinux and firewalld notes."
sources: ["https://docs.docker.com/engine/install/rhel/", "https://docs.docker.com/engine/install/fedora/", "https://docs.docker.com/engine/install/centos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Docker on RHEL and Fedora

RHEL-family systems can carry Podman and unofficial Docker packages, which Docker's install pages tell you to remove first.

## Remove conflicting packages
```bash
sudo dnf remove -y docker docker-client docker-client-latest docker-common docker-latest \
  docker-latest-logrotate docker-logrotate docker-engine podman runc
```
Docker's RHEL page includes `podman` and `runc` in the removal list; the Fedora page lists additional legacy packages, so check the page for your distro. Images and containers in `/var/lib/docker/` are not removed automatically.

## Add the repo and install
```bash
# RHEL 8/9/10 (Docker's CentOS page uses /linux/centos, Fedora uses /linux/fedora)
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
# Fedora: sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo docker run --rm hello-world
```
Pin a version:
```bash
dnf list docker-ce --showduplicates | sort -r
sudo dnf install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io docker-buildx-plugin docker-compose-plugin
# <VERSION_STRING> looks like 3:<version>-1.el9 (the .el9 suffix depends on your RHEL release)
```

## Platform notes
- **Firewall**: if you use ufw or firewalld, ports you publish from containers bypass those rules; Docker is only compatible with `iptables-nft` and `iptables-legacy`.
- **Start**: installing the packages does not start Docker and creates a `docker` group without adding users; run `sudo systemctl enable --now docker`.
- **Air-gapped**: download the five RPMs (`containerd.io`, `docker-ce`, `docker-ce-cli`, `docker-buildx-plugin`, `docker-compose-plugin`) from the download.docker.com `linux/rhel` tree (architecture, then `stable/Packages/`) and run `sudo dnf install ./<rpm> ...`.

## Verify
```bash
docker version --format '{{.Server.Version}}'
sudo docker run hello-world
rpm -q docker-ce containerd.io
```

## Gotchas
- `dnf config-manager` syntax differs: `--add-repo <url>` on the RHEL page, `addrepo --from-repofile <url>` on the Fedora page.
- Docker's RHEL page covers RHEL 8, 9 and 10 only.

## Checked

Checked against docker/docs `engine/install/rhel.md`, `fedora.md`, `centos.md` (docker/docs latest commit 2026-10-23, Engine 29).

- Removal list, repo URL and `dnf config-manager` forms, version-string format, `systemctl enable --now docker`, GPG fingerprint, supported RHEL versions (8, 9, 10), RPM list for manual installs, firewall limitations.
- Removed as unconfirmed: the podman-docker remark, `versionlock`, SELinux and firewalld zone notes, the cgroup v2 default note and the `container-selinux` verification.

Method: documentation only; no commands were run.
