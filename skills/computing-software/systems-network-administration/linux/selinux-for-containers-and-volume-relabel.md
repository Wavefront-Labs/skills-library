---
id: computing-software.systems-network-administration.linux.selinux-for-containers-and-volume-relabel
name: selinux-for-containers-and-volume-relabel
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, container-selinux, volume-relabel, container-t, svirt, udica, mcs-labels]
level: practitioner
status: docs-checked
description: "Run containers under SELinux: container_t and MCS separation, :z and :Z volume relabelling, container_file_t, booleans, custom policies with udica, and reading AVC denials."
sources:
  - https://github.com/containers/podman/blob/main/docs/source/markdown/options/volume.md
  - https://github.com/containers/udica/blob/main/README.md
  - https://github.com/containers/container-selinux/blob/main/container.te
  - https://github.com/docker/cli/blob/master/docs/reference/dockerd.md
  - https://github.com/kubernetes/website/blob/main/content/en/docs/tasks/configure-pod-container/security-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SELinux for containers and volume relabel

## Model
Podman and Docker (the daemon needs `--selinux-enabled`) start each container as `system_u:system_r:container_t:s0:c123,c456`. The MCS category pair is what separates containers from each other; content a container may use must carry a container file label such as `container_file_t`.

## Bind mounts
```bash
podman run -v /srv/app:/data:Z ...   # private label: only this container (or pod) can use it
podman run -v /srv/shared:/data:z ...# shared label: several containers can read/write it
ls -Z /srv/app
```
- Do not `:Z` or `:z` system files and directories: relabelling system content can make other confined services fail (podman docs). To mount something like your whole home directory, disable separation for that container instead. For your own data, use a dedicated directory, or label it manually: `semanage fcontext -a -t container_file_t '/srv/app(/.*)?' && restorecon -Rv /srv/app`.
- `:Z` is private: only the current container (or pod) can use the volume, so use `:z` when several containers share it.
- Relabelling walks every file under the volume and can delay container start on large trees; pre-label once with semanage instead.
- Files moved into a labelled volume can be fixed with `chcon -Rt container_file_t PATH`.
- Kubernetes: set `securityContext.seLinuxOptions`; see the Kubernetes security-context docs for `seLinuxChangePolicy`.

## Common booleans
```bash
setsebool -P container_manage_cgroup on    # let containers manage cgroups (systemd)
setsebool -P container_use_devices on      # use device volumes mounted into the container
getsebool -a | grep container
```

## Disable separation for one container (debug only)
`podman run --security-opt label=disable ...` disables SELinux separation for that container. Use it to confirm SELinux is the cause, then fix the label.

## Read denials
```bash
ausearch -m AVC -ts recent | audit2why
```
`scontext=...container_t:s0:c12,c34 tcontext=...user_home_t` = the volume isn't labelled for containers.

## Custom policy with udica
For a container that legitimately needs host paths or ports:
```bash
podman inspect app > app.json
udica -j app.json app_policy
semodule -i app_policy.cil /usr/share/udica/templates/{base_container.cil,net_container.cil,home_container.cil}
podman run --security-opt label=type:app_policy.process ...
```

## Verify
- [ ] `ps -eZ | grep container_t` shows distinct MCS pairs per container.
- [ ] No new AVCs after a functional test; SELinux remains Enforcing (`getenforce`).

## Checked
Checked 2026-10-26 against the podman volume option source (containers/podman main), the udica README, container-selinux container.te, the Docker dockerd reference and the Kubernetes security-context page.
Confirmed: :z shared versus :Z private labels, the warning not to relabel system content, `label=disable`, chcon -Rt container_file_t for moved files; the container_use_devices and container_manage_cgroup booleans (default false); the udica workflow (`podman inspect`, `udica -j`, `semodule -i` with the three template files, `--security-opt label=type:NAME.process`); `dockerd --selinux-enabled`; Kubernetes `seLinuxOptions` and `seLinuxChangePolicy`.
Removed as unconfirmed: CRI-O, the spc_t remark, the setroubleshoot journal command, host-service directory examples.
Method: documentation only; no commands were run.
