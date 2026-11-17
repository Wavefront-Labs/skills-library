---
id: computing-software.cloud-infrastructure-engineering.docker.rootless-docker-ports-and-limitations
name: rootless-docker-ports-and-limitations
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, rootless, rootless-mode, rootless-port-binding, rootless-privileged-ports, rootless-limitations, rootless-storage-driver, fuse-overlayfs, source-ip]
level: advanced
description: "Work around rootless Docker limits: binding ports below 1024, lost client source IPs, port driver choices, storage driver fallback and unsupported features."
sources: ["https://docs.docker.com/engine/security/rootless/tips/", "https://docs.docker.com/engine/security/rootless/troubleshoot/", "https://docs.docker.com/reference/cli/dockerd/", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rootless Docker: ports and limitations

## Privileged ports
`docker run -p 80:80` fails with `cannot expose privileged port 80`.
Options:
```sh
# host-wide: allow unprivileged binds to every port (affects all users)
echo 'net.ipv4.ip_unprivileged_port_start=0' | sudo tee /etc/sysctl.d/99-rootless.conf && sudo sysctl --system
# or grant only rootlesskit the capability
sudo setcap cap_net_bind_service=ep $(which rootlesskit)
systemctl --user restart docker
```
Or publish 8080 and forward 80 with a host firewall/redirect, or front it with a root-run proxy.

## Source IP and port drivers
`docker run -p` does not propagate source IP addresses by default (logs and rate limits see the
rootlesskit-side address). The fix depends on the RootlessKit version.

RootlessKit v3.0 or later: the `builtin` port driver propagates source IPs once Docker's
`userland-proxy` is disabled, in `~/.config/docker/daemon.json`:
```json
{"userland-proxy": false}
```
then `systemctl --user restart docker` (you may also need to load the `br_netfilter` kernel module).

Prior versions: use the `slirp4netns` port driver or the experimental `pasta` network driver with the
`implicit` port driver (needs Docker Engine 25.0 or later), set in
`~/.config/systemd/user/docker.service.d/override.conf`, then `systemctl --user daemon-reload` and restart:
```ini
[Service]
Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=pasta"
Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=implicit"
```
(for `slirp4netns`, set both `DOCKERD_ROOTLESS_ROOTLESSKIT_NET` and `DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER` to `slirp4netns`).

## Storage driver
Supported rootless storage drivers: `overlay2` (kernel 5.11 or later), `fuse-overlayfs` (kernel 4.18 or
later, package installed), `btrfs` (kernel 4.18 or later, or a `user_subvol_rm_allowed` mount) and `vfs`.
`docker info` shows which one you got.

## Not supported / degraded
- AppArmor, checkpoint, overlay networks (Swarm), SCTP port publishing.
- Resource limits (`--memory`, `--cpus`, `--pids-limit`) need cgroup v2 **and** systemd
  delegation of controllers to the user (`Delegate=cpu cpuset io memory pids` in
  `/etc/systemd/system/user@.service.d/delegate.conf`, then `systemctl daemon-reload`; delegating
  `cpuset` needs systemd 244 or later); otherwise rootless mode ignores the flags.
- Until Docker Engine v29.5, `--net=host` was the rootlesskit namespace, not the real host network.
- NFS-backed home directories break data-root (set a local `data-root` in `~/.config/docker/daemon.json`).
- Ping needs `net.ipv4.ping_group_range = 0   2147483647` in sysctl.

## Verify
`docker run -d -p 80:80 nginx` succeeds after the sysctl/setcap; `docker logs` of the nginx
shows real client IPs once source IP propagation is configured as above; `docker info` shows
`Cgroup Driver: systemd` (not `none`) when cgroup limits are usable.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main) Rootless Tips and Troubleshooting pages.
- Confirmed the privileged-port options (`net.ipv4.ip_unprivileged_port_start=0`, `setcap cap_net_bind_service=ep` on `rootlesskit`), the source-IP behaviour for RootlessKit v3.0+ (`userland-proxy: false`) and earlier (`slirp4netns` port driver, `pasta` + `implicit`, Docker Engine 25.0+), and the `DOCKERD_ROOTLESS_ROOTLESSKIT_NET` and `_PORT_DRIVER` variable names.
- Confirmed storage drivers and kernel gates, unsupported features, cgroup v2 + systemd delegation (`Delegate=cpu cpuset io memory pids`, systemd 244 for cpuset), the `--net=host` change in Engine v29.5, NFS data-root workaround and the ping sysctl.
- Removed the "very slow" vfs claim, "pasta preferred" advice and the memory-limit warning text.
Method: documentation only; no commands were run.
