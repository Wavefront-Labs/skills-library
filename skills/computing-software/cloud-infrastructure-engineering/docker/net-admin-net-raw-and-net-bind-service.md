---
id: computing-software.cloud-infrastructure-engineering.docker.net-admin-net-raw-and-net-bind-service
name: net-admin-net-raw-and-net-bind-service
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, capabilities, net-admin, net-raw, net-bind-service, cap-add, vpn-container]
level: advanced
status: docs-checked
description: "Decide on network capabilities: drop NET_RAW from the default set, when NET_ADMIN is truly needed (VPN, iptables, tc) and why non-root can bind low ports without NET_BIND_SERVICE."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://github.com/moby/moby/blob/master/daemon/oci_linux.go", "https://man7.org/linux/man-pages/man7/capabilities.7.html", "https://kubernetes.io/docs/concepts/security/pod-security-standards/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NET_ADMIN, NET_RAW and NET_BIND_SERVICE

## NET_RAW (in Docker's default set)
Allows RAW and PACKET sockets (per the `docker run` reference).
- Most apps never need it. Drop it: `--cap-drop NET_RAW` (or `--cap-drop ALL` and add back).
- `ping` can work without NET_RAW through unprivileged ICMP sockets: for containers with a private
  network namespace the daemon sets `net.ipv4.ping_group_range` to `0 2147483647`, except under
  userns-remap or when the daemon itself runs in a user namespace (Engine source, `oci_linux.go`).
- The Kubernetes restricted Pod Security Standard requires containers to drop ALL capabilities.

## NET_ADMIN (not in the default set)
Various network-related operations (capabilities(7)); the `docker run` reference says to use
`--cap-add=NET_ADMIN` rather than `--privileged` to modify network interfaces:
```bash
docker run -it --rm --cap-add=NET_ADMIN ubuntu:24.04 ip link add dummy0 type dummy
```
Scope: with a private network namespace it acts on the container's own namespace; with
`--network host` the container shares the **host** network namespace, so treat NET_ADMIN + host
network as control of the host's networking.

## NET_BIND_SERVICE and low ports
The daemon sets `net.ipv4.ip_unprivileged_port_start=0` inside containers with their own
network namespace (when the kernel has that sysctl), so a non-root process can bind port 80 without any
capability. You can drop NET_BIND_SERVICE in most cases.
Exceptions: `--network host` (host sysctl applies) and kernels/runtimes without that default;
then use `setcap cap_net_bind_service=ep /app/server` in the image or listen on >1024.

## Recommended baseline
```bash
docker run --cap-drop ALL --cap-add CHOWN --cap-add SETUID --cap-add SETGID app   # only what the image's entrypoint needs
```
Find what is needed by starting with `--cap-drop ALL` and reading the errors
(`Operation not permitted`), not by adding broad capabilities.

## Verify
```bash
docker inspect -f '{{.HostConfig.CapAdd}} {{.HostConfig.CapDrop}}' <c>
docker exec <c> sh -c 'grep CapEff /proc/1/status'
```

## Checked
Date: 2026-10-24. Documentation: Docker docs `docker run` reference (docker/docs main), moby/moby `daemon/oci_linux.go` (master), man-pages capabilities(7), Kubernetes Pod Security Standards page.
- Confirmed NET_RAW is in the default set and means RAW and PACKET sockets, NET_ADMIN is not in the default set and is the documented alternative to `--privileged`, and the `ip link add dummy0` example.
- Confirmed the daemon-set sysctls `net.ipv4.ping_group_range=0 2147483647` and `net.ipv4.ip_unprivileged_port_start=0` for private network namespaces (with the userns-remap exception for ping) in the Engine source.
- Confirmed the restricted Pod Security Standard drops ALL capabilities.
- Removed the version gate, spoofing claims, WireGuard and `tc netem` examples and the sysctl `src_valid_mark` flag, none of which a checked source covers.
Method: documentation only; no commands were run.
