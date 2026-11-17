---
id: computing-software.cloud-infrastructure-engineering.docker.cgroup-parent-and-cgroup-driver
name: cgroup-parent-and-cgroup-driver
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, cgroups, cgroup-parent, cgroup-driver, systemd-slice, resource-limits, cgroup-v2]
level: advanced
status: docs-checked
description: "Group container resources under a parent cgroup or systemd slice with --cgroup-parent, choose the systemd vs cgroupfs cgroup driver, and verify limits on cgroup v2 hosts."
sources: ["https://docs.docker.com/reference/cli/dockerd/#default-cgroup-parent", "https://docs.docker.com/reference/cli/dockerd/#configure-cgroup-driver", "https://github.com/compose-spec/compose-spec/blob/main/spec.md", "https://www.freedesktop.org/software/systemd/man/latest/systemd.slice.html", "https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# --cgroup-parent and the cgroup driver

## Cgroup driver
| Driver | Who manages cgroups | Container cgroup path |
|---|---|---|
| `systemd` | systemd (scope units) | `system.slice/docker-<id>.scope` |
| `cgroupfs` | dockerd writes cgroupfs directly | `/docker/<id>` |

If `native.cgroupdriver` is omitted, Docker uses `cgroupfs` on cgroup v1 hosts and `systemd` on cgroup v2 hosts where systemd is available; asking for `systemd` where it is not available makes the daemon error out. Set explicitly if needed:
```json
{ "exec-opts": ["native.cgroupdriver=systemd"] }
```
If `--cgroup-parent` is not set, the daemon default is `/docker` for the cgroupfs driver and `system.slice` for the systemd driver.

## Grouping containers under a budget
With the systemd driver, `--cgroup-parent` must be a **slice** name:
```ini
# /etc/systemd/system/batch.slice
[Slice]
CPUQuota=200%
MemoryMax=8G
IOWeight=50
```
```bash
sudo systemctl daemon-reload && sudo systemctl start batch.slice
docker run -d --cgroup-parent=batch.slice --memory 2g worker:1.0
docker run -d --cgroup-parent=batch.slice --memory 2g worker:1.0
# all batch containers share at most 2 CPUs and 8 GiB, each also capped at 2 GiB
```
Compose: `cgroup_parent: batch.slice`. The daemon-wide default is the `cgroup-parent` key in `daemon.json` (or `dockerd --cgroup-parent`); the per-container option overrides it.

With cgroupfs, a leading slash (`--cgroup-parent=/batch`) creates the cgroup under the root cgroup; without one it is created under the daemon's own cgroup.

## Verify
```bash
docker info -f '{{.CgroupDriver}} {{.CgroupVersion}}'
systemctl status batch.slice --no-pager            # aggregated memory and CPU
docker inspect -f '{{.HostConfig.CgroupParent}}' <c>
```

## Gotchas
- With the systemd driver `--cgroup-parent` must be a slice name (for example `batch.slice`), not a path such as `/batch`.
- Nested slices use dashes: `batch-nightly.slice` lives under `batch.slice`.

## Checked

Checked against the docker/docs repository (dockerd reference, `dockerd.md`, latest commit 2026-10-23, Engine 29 documentation), the Engine API swagger and the Compose Specification.

- Driver default: `cgroupfs` on cgroup v1, `systemd` on cgroup v2 with systemd available; only `cgroupfs` and `systemd` are accepted (dockerd reference, "Configure cgroup driver").
- `--cgroup-parent` defaults (`/docker`, `system.slice`), leading-slash rule, slice-name rule and dash nesting (dockerd reference, "Default cgroup parent").
- `CgroupDriver`, `CgroupVersion` (`docker info`) and `HostConfig.CgroupParent` exist in the Engine API; `cgroup_parent` exists in the Compose Specification.
- `CPUQuota=`, `MemoryMax=` and `IOWeight=` are systemd resource-control settings (systemd.resource-control man page source).
- Removed as unconfirmed: the verbatim error text, the Kubernetes kubelet statement, the rootless delegation line, the driver-change restart line and the cgroup file path commands.

Method: documentation only; no commands were run.
