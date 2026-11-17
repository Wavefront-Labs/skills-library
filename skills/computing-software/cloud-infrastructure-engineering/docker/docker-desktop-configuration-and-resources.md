---
id: computing-software.cloud-infrastructure-engineering.docker.docker-desktop-configuration-and-resources
name: docker-desktop-configuration-and-resources
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-desktop, desktop, wsl2, file-sharing, wslconfig, virtiofs, vmmem, resource-limits, macos, windows, bind-mount-performance, host-docker-internal, docker-desktop-settings]
level: practitioner
status: docs-checked
description: "Tuning Docker Desktop on macOS and Windows: WSL2 memory via .wslconfig, file-sharing backends (VirtioFS/gRPC FUSE, WSL paths vs /mnt/c), reclaiming disk from the VM image, and host.docker.internal."
sources: ["https://docs.docker.com/desktop/settings-and-maintenance/settings/", "https://docs.docker.com/desktop/features/networking/networking-how-tos/", "https://learn.microsoft.com/en-us/windows/wsl/wsl-config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Desktop configuration and resources

**Goal:** Desktop stops eating the laptop (RAM, disk), bind mounts are fast enough for
hot-reload dev, and containers can reach services on the host.

## Where the limits actually live
Docker Desktop runs the engine in a Linux VM. The CPU and memory you set are the VM's, shared
by every container.
- **Mac, Linux, Windows Hyper-V backend**: Settings, Resources: **CPU limit**, **Memory limit**
  (defaults to 50% of the host's memory), **Swap** (1 GB default), **Disk usage limit**, **Disk
  image location**, and **Resource Saver** (turns the Linux VM off automatically when Docker
  Desktop is idle).
- **Windows WSL 2 backend**: in WSL 2 mode, configure memory, CPU and swap limits on the WSL 2
  utility VM with `.wslconfig` in your Windows user profile folder:
  ```ini
  [wsl2]
  memory=8GB
  processors=4
  swap=2GB
  localhostForwarding=true
  ```
  `memory` defaults to 50% of total memory on Windows; `processors` defaults to the number of
  logical processors; `localhostForwarding` defaults to `true`; `swap` defaults to 25% of memory
  rounded up to the nearest GB. Run `wsl --shutdown` (this shuts down ALL running WSL
  distributions) and restart Docker Desktop for the change to take effect.

## File sharing: the bind-mount performance problem
Bind mounts cross the VM boundary.
- **Mac**: Settings, General, file sharing implementation (with the Apple Virtualization
  framework VMM): **VirtioFS** (default) or **gRPC FUSE**; the docs recommend VirtioFS for speedy
  file sharing. Under Resources, **Virtual file shares** default to `/Users`, `/Volumes`,
  `/private`, `/tmp` and `/var/folders`; a project outside the list must be added or you may get
  `Mounts denied`. Sharing too many files can cause high CPU load and slow performance.
  **Synchronized file shares** improve bind mount performance using synchronized filesystem caches
  (Mac, Linux, Windows Hyper-V; see the docs for plan availability).
- **Windows WSL 2**: enable "Use the WSL 2 based engine" and select the distributions to
  integrate under Resources, WSL integration (integration is enabled on your default WSL
  distribution by default). Run `docker` from the WSL shell.
- Named volumes (`-v data:/app/data`) live inside the VM; use them for databases and caches and
  bind-mount only source code.

## Disk reclaim
```bash
docker system df                        # what's using it
docker system prune -a --volumes        # reclaim inside the VM (removes unused images and anonymous volumes)
```
Settings, Resources has a **Disk usage limit** and **Disk image location**; the docs warn that
moving the disk image has consequences, so read the setting's notes first.

## Host networking from containers
- `host.docker.internal` resolves to the internal IP address of your host and
  `gateway.docker.internal` to the gateway IP of the Docker VM (Docker Desktop). On Linux Engine add
  `--add-host=host.docker.internal:host-gateway`.
- **Enable host networking** (Settings, Resources, Network) lets containers started with `--net=host`
  use `localhost` to reach TCP and UDP services on the host and vice versa; the settings table lists it
  for Mac.
- **Docker subnet** (Settings, Resources, Network) defaults to `192.168.65.0/24`; change it to avoid
  conflicts with your environment.
- Kubernetes: Settings, Kubernetes, enable.

## Daemon configuration
The Docker Engine settings tab edits `$HOME/.docker/daemon.json`; options are those in the
`dockerd` reference. Proxy settings live under Resources, Proxies.

## Verify
```bash
docker info --format '{{.NCPU}} {{.MemTotal}}'      # the VM's limits, matching the settings or .wslconfig
docker run --rm alpine ping -c1 host.docker.internal
```

## Checked

Date: 2026-10-24. Documentation release: Docker Desktop settings and networking pages (docker/docs main) and the Microsoft WSL configuration page.
Confirmed: Resources settings (memory default 50%, swap default 1 GB, Resource Saver, disk settings), WSL 2 mode
using `.wslconfig` and its `memory`, `processors`, `swap` and `localhostForwarding` defaults, `wsl --shutdown` shutting down all
distributions, VirtioFS/gRPC FUSE choice and VirtioFS default, default virtual file shares and `Mounts denied`, Synchronized
file shares, WSL integration default, `host.docker.internal` and `gateway.docker.internal`, the host networking setting
and its Mac platform listing, Docker subnet default, and the `$HOME/.docker/daemon.json` location. Removed: speed
multipliers, disk image file names and compaction commands, vmmem behaviour, the Desktop version gates, Rosetta
speed claims, osxfs and consistency-flag claims, and troubleshooting recipes not backed by the docs.

Method: documentation only; no commands were run.
