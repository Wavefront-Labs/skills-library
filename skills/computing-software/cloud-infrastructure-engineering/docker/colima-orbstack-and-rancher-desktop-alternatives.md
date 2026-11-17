---
id: computing-software.cloud-infrastructure-engineering.docker.colima-orbstack-and-rancher-desktop-alternatives
name: colima-orbstack-and-rancher-desktop-alternatives
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-desktop-alternatives, colima, orbstack, rancher-desktop, lima, docker-context, macos, testcontainers-docker-host, cli-plugins]
level: practitioner
status: gated
description: "Replace Docker Desktop with Colima, OrbStack or Rancher Desktop: install, sockets and contexts, compose/buildx plugins, Testcontainers settings, migrating images and volumes."
sources: ["https://github.com/abiosoft/colima", "https://github.com/abiosoft/colima/blob/main/docs/FAQ.md", "https://docs.orbstack.dev/", "https://docs.rancherdesktop.io/", "https://java.testcontainers.org/supported_docker_environment/", "https://www.docker.com/pricing/faq/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colima, OrbStack and Rancher Desktop as Docker Desktop alternatives

**Why switch:** Docker Desktop needs a paid subscription in companies over 250 employees or
$10M revenue, and some teams want a lighter VM. All three alternatives run a Linux VM with
`dockerd` and expose a socket the normal `docker` CLI talks to.

| | Colima | OrbStack | Rancher Desktop |
|---|---|---|---|
| Platforms | macOS, Linux | macOS | macOS, Windows, Linux |
| Engine | dockerd or containerd (+nerdctl) | dockerd | dockerd (moby) or containerd |
| Kubernetes | k3s (`--kubernetes`) | built-in k8s | k3s, version picker |
| Licence | MIT | commercial for business use | Apache 2.0 |
| Socket | `~/.colima/default/docker.sock` | `~/.orbstack/run/docker.sock` | `~/.rd/docker.sock` |

## Colima
```bash
brew install colima docker docker-compose docker-buildx
colima start --cpu 4 --memory 8 --disk 100 --vm-type vz --vz-rosetta --mount-type virtiofs
docker context ls          # colima context is created and selected
colima start --kubernetes  # optional k3s
colima ssh                 # into the VM; colima status / colima delete
```
Homebrew installs compose/buildx as plugins outside the default dir; tell the CLI:
```json
// ~/.docker/config.json
{ "cliPluginsExtraDirs": ["/opt/homebrew/lib/docker/cli-plugins"] }
```
Resources are fixed at create time on older versions: `colima stop && colima start --cpu 6`
reapplies; disk can only grow.

## OrbStack
Install the app, then `docker context use orbstack`. Containers get `<name>.orb.local`
domains and the VM shares host networking well; `orb` CLI also runs full Linux machines.
It imports Docker Desktop data on first run (offers to migrate images/volumes).

## Rancher Desktop
Preferences → Container Engine → **dockerd (moby)** for `docker` CLI compatibility
(containerd mode uses `nerdctl` and a different image namespace). Disable Kubernetes if you
only need containers.

## Testcontainers and other socket consumers
Tools that hardcode `/var/run/docker.sock` need the real socket:
```bash
export DOCKER_HOST=unix://$HOME/.colima/default/docker.sock
export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock   # path inside the VM for Ryuk
# Colima only, if containers must be reached by IP:  colima start --network-address
export TESTCONTAINERS_HOST_OVERRIDE=$(colima ls -j | jq -r '.address')
```
OrbStack and Rancher Desktop can create the `/var/run/docker.sock` symlink for you (admin
option), which avoids most of this.

## Migrating from Docker Desktop
Images: `docker save` the local-only ones before uninstalling, or just re-pull/rebuild.
Volumes do not transfer automatically: export with a helper container
(`docker run --rm -v vol:/v -v $PWD:/b alpine tar czf /b/vol.tgz -C /v .`) on the old
context, import on the new. Remove Desktop's leftover `credsStore: desktop` from
`~/.docker/config.json` or `docker login` errors with "docker-credential-desktop not found".

## Verify
```bash
docker context show && docker info -f '{{.OperatingSystem}} {{.NCPU}} {{.MemTotal}}'
docker compose version && docker buildx version
docker run --rm -v "$PWD":/w alpine ls /w     # file sharing works
```

## Checked

- Date: 2026-11-02.
- Confirmed against: colima start flags --cpu, --memory, --disk, --vm-type, --vz-rosetta, --kubernetes, --network-address (Colima README and FAQ).
- Not confirmed: socket paths for OrbStack and Rancher Desktop, --mount-type, cliPluginsExtraDirs and credsStore advice (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
