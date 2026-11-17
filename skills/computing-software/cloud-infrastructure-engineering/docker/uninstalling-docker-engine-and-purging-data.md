---
id: computing-software.cloud-infrastructure-engineering.docker.uninstalling-docker-engine-and-purging-data
name: uninstalling-docker-engine-and-purging-data
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-uninstall, engine-install, purge, var-lib-docker, iptables, cleanup]
level: practitioner
status: docs-checked
description: "Remove Docker Engine completely: purge packages, data-root and containerd state, leftover iptables chains, bridges, users and config, while keeping data you need."
sources: ["https://docs.docker.com/engine/install/ubuntu/#uninstall-docker-engine", "https://docs.docker.com/engine/install/rhel/#uninstall-docker-engine", "https://docs.docker.com/engine/security/rootless/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uninstalling Docker Engine and purging data

Packages remove binaries only. Images, containers, volumes and networks stay in the data
root until you delete them.

## 1. Save what matters first
```bash
docker volume ls
docker run --rm -v dbdata:/v -v $PWD:/b alpine tar czf /b/dbdata.tgz -C /v .   # per needed volume
docker save -o images.tar <image>[:tag] ...
```

## 2. Stop and remove packages
```bash
sudo systemctl disable --now docker.service docker.socket containerd.service
# Debian/Ubuntu
sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin \
  docker-compose-plugin docker-ce-rootless-extras
# RHEL/Fedora
sudo dnf remove -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
```

## 3. Delete state
```bash
DR=$(docker info -f '{{.DockerRootDir}}' 2>/dev/null || echo /var/lib/docker)   # run before step 2 if possible
sudo rm -rf "$DR" /var/lib/containerd
# Debian/Ubuntu: source list and keyring
sudo rm /etc/apt/sources.list.d/docker.sources /etc/apt/keyrings/docker.asc
```
Docker's page says you must delete edited configuration files (for example `/etc/docker/daemon.json`) yourself. A custom `data-root` (check `daemon.json` before deleting it) is not covered by the default path.

## 4. Network leftovers
Docker's uninstall pages do not cover bridges or firewall rules. Review them with your distribution's tools (`ip link`, `iptables`, `nft`) before removing anything by hand, or reboot and confirm that nothing is recreated.


## 5. Users and groups
The `docker` group created by the packages is not covered by Docker's uninstall pages; remove it with your distribution's group tools only if nothing else uses it.
Rootless installs: `dockerd-rootless-setuptool.sh uninstall` removes the systemd service but not binaries or data; remove the data with `rootlesskit rm -rf ~/.local/share/docker`.

## Verify
```bash
command -v docker dockerd containerd || echo "binaries gone"
ls /var/lib/docker /var/lib/containerd
```

## Gotchas
- Docker Desktop for Linux is a separate product with its own uninstall steps.

## Checked

Checked against docker/docs `engine/install/ubuntu.md` and `rhel.md` (Uninstall Docker Engine sections), the rootless mode pages and the Engine API swagger (`DockerRootDir`) (docker/docs latest commit 2026-10-23, Engine 29).

- Package lists for `apt purge` and `dnf remove`, deleting `/var/lib/docker` and `/var/lib/containerd`, `docker.sources` and `docker.asc` removal, and the statement that edited config files must be deleted by hand.
- Rootless: `dockerd-rootless-setuptool.sh uninstall` does not remove binaries or data; `rootlesskit rm -rf ~/.local/share/docker` removes data.
- `docker info -f '{{.DockerRootDir}}'` is a valid field.
- Removed as unconfirmed: bridge and iptables cleanup commands, the legacy `docker.list` and `docker-ce.repo` paths, snap removal and the `~/.docker` and `/etc/docker` blanket deletes, and the group removal command.

Method: documentation only; no commands were run.
