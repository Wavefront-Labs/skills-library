---
id: computing-software.cloud-infrastructure-engineering.docker.binding-privileged-ports-as-non-root
name: binding-privileged-ports-as-non-root
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, non-root, unprivileged-ports, ip-unprivileged-port-start, net-bind-service, port-publishing, sysctl]
level: practitioner
description: "Let a non-root container serve on port 80/443: listen high and publish, the net.ipv4.ip_unprivileged_port_start sysctl, or NET_BIND_SERVICE with setcap."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/reference/compose-file/services/", "https://github.com/moby/moby/blob/master/daemon/oci_linux.go", "https://docs.docker.com/engine/security/rootless/tips/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Binding ports below 1024 as non-root

Symptom: `bind: permission denied` / `EACCES` on `:80` after adding `USER 10001`.

## Option 1 - listen high, publish low (preferred)
```sh
docker run -p 80:8080 app:1          # app listens on 8080 inside
```
The host-side bind is done by dockerd (root) or iptables DNAT, so the container never needs
the privilege. In Kubernetes, the Service maps 80 -> 8080.

## Option 2 - lower the unprivileged port floor in the container's netns
```sh
docker run --sysctl net.ipv4.ip_unprivileged_port_start=0 -p 80:80 app:1
```
```yaml
services:
  web:
    sysctls:
      net.ipv4.ip_unprivileged_port_start: 0
```
This sysctl is per network namespace, so it only affects the container. The Engine source
(`daemon/oci_linux.go`) already sets it to 0 for containers with a private network namespace when
the kernel has the sysctl (so this often "just works"); explicit is safer when images run on
other runtimes. `net.*` sysctls are not allowed with `--network=host`.

## Option 3 - file capability on the binary
```dockerfile
RUN setcap cap_net_bind_service=ep /usr/sbin/nginx
USER 10001
```
`setcap` comes from libcap (for example the `libcap2-bin` package on Debian-based images). Requires
`NET_BIND_SERVICE` in the bounding set (it is in Docker's default set); `execve` fails with `EPERM` if
you `--cap-drop ALL` without `--cap-add NET_BIND_SERVICE`.

## Which to pick
| Situation | Use |
|---|---|
| You control the app port | Option 1 |
| Image hardcodes 80 (nginx default conf) | change config to 8080, or Option 2 |
| Host networking | Option 3 or bind high |
| Rootless Docker host-side < 1024 | host sysctl `net.ipv4.ip_unprivileged_port_start=0` or `setcap cap_net_bind_service=ep` on `rootlesskit` |

## Verify
```sh
docker run --rm app:1 sh -c 'cat /proc/sys/net/ipv4/ip_unprivileged_port_start'   # 0 in a private network namespace
docker run --rm --user 10001 app:1                                                  # the app binds :80 without error
```

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main: `docker run` reference, Compose services reference, Rootless Tips), moby/moby `daemon/oci_linux.go` (master), man-pages capabilities(7).
- Confirmed `--sysctl` and Compose `sysctls`, that `net.*` sysctls are not allowed with `--network=host`, and that the daemon sets `net.ipv4.ip_unprivileged_port_start=0` for private network namespaces (source, only when the sysctl exists).
- Confirmed the `setcap cap_net_bind_service=ep` form and the `EPERM` rule for file capabilities outside the bounding set, and the rootless host options.
- Removed the "20.10+" version gate, the `no-new-privileges`/setuid sentence and the busybox `nc` check, which no checked source covers.
Method: documentation only; no commands were run.
