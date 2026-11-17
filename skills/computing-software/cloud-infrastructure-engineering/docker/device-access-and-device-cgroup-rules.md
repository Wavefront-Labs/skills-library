---
id: computing-software.cloud-infrastructure-engineering.docker.device-access-and-device-cgroup-rules
name: device-access-and-device-cgroup-rules
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, device-flag, device-cgroup-rule, usb-serial, hotplug, group-add, cdi, privileged-alternative, compose-devices]
level: advanced
status: docs-checked
description: "Give containers hardware access without --privileged: --device for fixed nodes, --device-cgroup-rule plus /dev mounts for hotplug, group permissions, CDI devices, and rootless limits."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/reference/compose-file/services/", "https://docs.docker.com/reference/cli/dockerd/", "https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/devices.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device access: --device and device cgroup rules

**Goal:** a container talks to a serial adapter, USB device, camera or GPU render node with
the minimum privilege, including devices plugged in after start.

## Fixed device: `--device`
```bash
docker run --device /dev/ttyUSB0:/dev/ttyUSB0:rwm --group-add dialout myimage
```
- `--device HOST:CONTAINER[:rwm]` makes the device usable without `--privileged`; by default the container can
  read, write and `mknod` it (`r`, `w`, `m`; for example `:r` for read-only).
- Docker assigns devices at container creation time (they are added to the cgroup allow list and created
  in the container), so a device plugged in later is not there; see the hotplug rule below.
- Non-root container users need a group that can open the node: use `--group-add` with the group name
  or a numeric gid (a numeric gid does not depend on the image's `/etc/group`).

## Hotplug: device cgroup rule + /dev bind
```bash
ls -l /dev/ttyUSB0          # crw-rw---- 1 root dialout 188, 0 ... -> char major 188
docker run -d --device-cgroup-rule='c 188:* rmw' --name my-container my-image
```
This is the documented approach for devices that appear after start: add a more permissive rule for a
major number with any minor, then have `udev` run a script that does
`docker exec my-container mknod newDevX c 188 <minor>` when a device is added. Devices present at start
still have to be passed explicitly with `--device`. The rule format is the kernel's device cgroup format
(`type major:minor access`, with `c`/`b`/`a`, `*` wildcards and `r`, `w`, `m`). Major numbers come from the
kernel devices list (188 is USB serial converters, 166 ACM USB modems, 81 video4linux, 226 DRI); read the
major from `ls -l` on your node.

## Compose
```yaml
services:
  modbus:
    devices: ["/dev/ttyUSB0:/dev/ttyUSB0"]
    group_add: ["20"]
  camera:
    devices: ["/dev/video0:/dev/video0"]
    device_cgroup_rules: ["c 81:* rmw"]
```

## CDI devices (vendor-described)
CDI is enabled by default since Docker Engine 28.3.0 (Linux containers only). Reference a device by its
fully-qualified name:
```bash
docker run --device=vendor.com/class=device-name --rm -it ubuntu
```
This needs a CDI specification (JSON or YAML) for the device in a CDI spec directory on the daemon host:
the defaults are `/etc/cdi/` for static specs and `/var/run/cdi` for generated ones; change them with the
`cdi-spec-dirs` daemon option. The spec can also set environment variables, host mounts and hooks. Disable
CDI with `"features": {"cdi": false}` in `daemon.json`; `docker info` shows the CDI status.

## Why not `--privileged`
`--privileged` gives all capabilities, enables access to all devices on the host and reconfigures
AppArmor or SELinux, so the container gets nearly the same access to the host as host processes.
`--device` plus a group is the documented way to give access to specific devices.

## Gotchas
- Rootless Docker: the daemon user must have OS-level access to the device node.
- Devices present at start must still be added with `--device`; the cgroup rule alone does not create nodes.

## Verify
```bash
docker exec modbus ls -l /dev/ttyUSB0 && docker exec modbus id
```

## Checked
Date: 2026-10-24. Documentation: Docker docs `docker run` reference (`--device`, `--device-cgroup-rule`, `--privileged`, CDI), `dockerd` reference (CDI configuration), Compose services reference (`devices`, `device_cgroup_rules`, `group_add`), Linux kernel `admin-guide/devices.txt`.
- Confirmed `--device` syntax and `rwm` permissions, the `--device-cgroup-rule` hotplug pattern with `udev` and `docker exec ... mknod`, CDI behaviour (enabled by default since Engine 28.3.0, default spec directories, `cdi-spec-dirs`, `features.cdi`), `--privileged` semantics, and Compose `devices` and `device_cgroup_rules` syntax.
- Confirmed the kernel major numbers 188, 166, 81 and 226; the kernel list names 189 "USB serial converters - alternate devices", so the `/dev/bus/usb` major claim was removed.
- Removed the symlink-resolution, `docker update`, cgroup v2/eBPF, Docker Desktop/`usbipd`, udev rule, `nvidia-ctk` and `stty` claims that no checked source covers.
Method: documentation only; no commands were run.
