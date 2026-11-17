---
id: computing-software.cloud-infrastructure-engineering.etcd.install-and-containers
name: install-and-containers
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [install, binary, docker, container, podman, image, gcr, etcd-development, static-bootstrap]
level: practitioner
status: docs-checked
description: "Install etcd from release binaries or source, or run it in Docker with the static bootstrap examples and ports 2379 and 2380."
sources:
  - "https://etcd.io/docs/v3.5/install/"
  - "https://etcd.io/docs/v3.5/op-guide/container/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Install page options:

- Pre-built binaries (the easiest way): download the archive for your platform from Releases (the page says v3.5.21 or later), unpack it, put the binaries on your PATH (for example `/usr/local/bin`) and test with `etcd --version`.
- Build from source: clone the etcd repository at a release tag, run `./build.sh`; the binaries are under `bin`. Add that directory to your PATH.
- OS packages can deliver outdated versions and are not officially supported; for many Linux distributions this is strongly discouraged. The recommended Linux routes are pre-built binaries or Homebrew (`brew install etcd`, also on macOS).

Container registries: `gcr.io/etcd-development/etcd` is the primary registry and `quay.io/coreos/etcd` the secondary.

Single node from the container guide (host IP in `NODE1`, volume `etcd-data`):

```bash
docker run -p 2379:2379 -p 2380:2380 --volume=${DATA_DIR}:/etcd-data --name etcd ${REGISTRY}:${ETCD_VERSION} /usr/local/bin/etcd --data-dir=/etcd-data --name node1 --initial-advertise-peer-urls http://${NODE1}:2380 --listen-peer-urls http://0.0.0.0:2380 --advertise-client-urls http://${NODE1}:2379 --listen-client-urls http://0.0.0.0:2379 --initial-cluster node1=http://${NODE1}:2380
```

- To expose the API to clients outside the Docker host, use the host IP address when configuring etcd (or run with `--net=host`).
- Store data on a Docker volume (`docker volume create --name etcd-data`).
- Check with `etcdctl --endpoints=http://${NODE1}:2379 member list`, or run `docker exec etcd /usr/local/bin/etcdctl put foo bar`.
- A three-node cluster runs one container per machine with the same `--initial-cluster` list (name=http://host:2380 entries), `--initial-cluster-state new` and a shared `--initial-cluster-token`; each uses its own `--name` and its own IP in the advertise URLs. Ports: 2379 for clients, 2380 for peers.
- The release container does not include default root certificates; mount a certificate bundle (for example `/etc/ssl/certs/ca-certificates.crt`) into the container to use HTTPS with certificates trusted by a root authority.

## Checked

2026-11-08. Read in full: etcd v3.5 Install page and the container guide. Confirmed install routes, registries, the run command shape and the cluster flags. Removed: the archive contents listing, `etcdctl version` check, the same-version, restart-policy and image-pinning advice, the distinct-host-port rule and the minor-version upgrade remark (not on the pages read).
Method: documentation only; no commands were run.
