---
id: computing-software.cloud-infrastructure-engineering.docker.installing-docker-engine-on-linux
name: installing-docker-engine-on-linux
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, engine-install, apt-repo-install, docker-ce-version-pin, get-docker-sh, convenience-script, docker-group, post-install]
level: practitioner
description: "Install Docker Engine from Docker's apt/dnf repository with a pinned version, know when get.docker.com is acceptable, and do post-install steps like the docker group."
sources: ["https://docs.docker.com/engine/install/ubuntu/", "https://docs.docker.com/engine/install/rhel/", "https://docs.docker.com/engine/install/fedora/", "https://docs.docker.com/engine/install/linux-postinstall/", "https://github.com/docker/docker-install"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing Docker Engine on Linux

## Debian/Ubuntu from Docker's repository
```sh
# conflicting unofficial packages: docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd runc
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd runc | cut -f1)
sudo apt update && sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update
apt list --all-versions docker-ce                      # available versions
VERSION_STRING=5:<version>-1~ubuntu.24.04~noble       # from the list above
sudo apt install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io \
  docker-buildx-plugin docker-compose-plugin
```
Omit the version strings to install the latest. Docker's page says Ubuntu derivatives such as Linux Mint are not officially supported. Debian: use the Debian page's URL (`https://download.docker.com/linux/debian`) and its suite instructions.

## RHEL/Fedora/CentOS Stream
```sh
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
dnf list docker-ce --showduplicates | sort -r
sudo dnf install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```
Omit the version strings to install the latest. Docker documents RHEL 8, 9 and 10, and uses the `linux/centos` and `linux/fedora` repo URLs on those distros; on Fedora the command is `sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo`. When prompted, check the GPG fingerprint matches `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`.

## get.docker.com convenience script
```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh --dry-run          # read what it will do
sudo sh get-docker.sh --version <VERSION>
```
Docker recommends it only for test and development: it needs root, installs the latest stable release by default (possible unexpected major upgrades), installs dependencies without asking, and is not designed to upgrade an existing installation (upgrade with the package manager instead). `get.docker.com/rootless` installs rootless mode; `test.docker.com` installs from the test channel.

## Post-install
```sh
sudo usermod -aG docker "$USER" && newgrp docker      # or log out/in
docker run --rm hello-world
sudo systemctl enable docker.service containerd.service
```
The `docker` group grants root-level privileges. On shared or
production hosts consider rootless Docker or sudo; Docker's post-install page also describes a group-password and `newgrp` approach.

## Gotchas
- Unofficial distribution packages (`docker.io` and others) conflict with Docker's packages: remove them first.
- When you publish container ports, Docker's rules bypass ufw and firewalld rules; Docker is compatible only with `iptables-nft` and `iptables-legacy`, and rules created with `nft` are not supported with Docker installed.
- `docker-ce-rootless-extras` is only needed for rootless mode.

## Verify
`docker version` shows both client and server; `sudo docker run hello-world` prints the confirmation message; `sudo systemctl status docker` shows the service running.

## Checked

Checked against docker/docs `engine/install/ubuntu.md`, `rhel.md`, `fedora.md`, `linux-postinstall.md`, the shared convenience-script include, and the docker-install `install.sh` (docker/docs latest commit 2026-10-23, Engine 29).

- Conflicting-package list, deb822 `docker.sources` repository setup, `apt list --all-versions docker-ce`, version-string formats (`5:<version>-1~ubuntu.24.04~noble`, `docker-ce-3:<version>-1.el9`), the `dnf` repo commands and the dnf5 Fedora form, GPG fingerprint.
- Convenience script limitations, `--dry-run`, `--version`, `--channel`, rootless script; post-install `usermod`, `newgrp`, `systemctl enable` lines; firewall limitations.
- Removed as unconfirmed: the pinned example Engine version, `apt-mark hold`, the `moby-engine` remark and the overlay2/cgroup v2 expectation.

Method: documentation only; no commands were run.
