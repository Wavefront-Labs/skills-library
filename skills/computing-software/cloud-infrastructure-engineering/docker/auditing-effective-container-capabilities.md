---
id: computing-software.cloud-infrastructure-engineering.docker.auditing-effective-container-capabilities
name: auditing-effective-container-capabilities
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, capabilities, capsh, cap-audit, pscap, file-capabilities, privileged-container]
level: advanced
status: docs-checked
description: "Audit real container capabilities: CapAdd/CapDrop/Privileged across a host, decoding /proc CapEff with capsh, pscap/getpcaps on the host, and file caps in images."
sources: ["https://man7.org/linux/man-pages/man7/capabilities.7.html", "https://man7.org/linux/man-pages/man1/capsh.1.html", "https://docs.docker.com/reference/cli/docker/container/run/", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing effective container capabilities

## Host-wide inventory from the API
```bash
docker ps -q | xargs docker inspect -f \
  '{{.Name}} priv={{.HostConfig.Privileged}} add={{.HostConfig.CapAdd}} drop={{.HostConfig.CapDrop}} user={{.Config.User}} net={{.HostConfig.NetworkMode}} pid={{.HostConfig.PidMode}}'
```
Flag: `priv=true`, `add=[SYS_ADMIN ...]`, `NET_ADMIN` with `net=host`, `pid=host`, empty
`drop` (full default set).

## What the process actually holds
```bash
docker exec <c> grep -E '^Cap(Inh|Prm|Eff|Bnd|Amb)' /proc/1/status
# CapEff: 00000000a80425fb   <- Docker's default set when running as root
capsh --decode=00000000a80425fb
# 0x00000000a80425fb=cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap
```
- A non-root process normally has `CapEff: 0000000000000000` even if the bounding set (`CapBnd`)
  is the default; capabilities added with `--cap-add` reach it only via file capabilities or
  ambient caps.
- `--privileged` gives the container all capabilities, so `CapEff` shows every capability bit the kernel supports (the value depends on the kernel).

From the host (no tools needed in the image), read the same fields for the container's init process:
```bash
pid=$(docker inspect -f '{{.State.Pid}}' <c>)
grep -E '^Cap(Inh|Prm|Eff|Bnd|Amb)' /proc/$pid/status
```

## File capabilities inside images
```bash
docker run --rm --entrypoint sh <image> -c 'getcap /path/to/binary'
# /path/to/binary cap_net_bind_service=ep
```
File capabilities are stored in the `security.capability` extended attribute and are applied at `execve`
(capabilities(7)). The file's permitted set is intersected with the thread's bounding set, so `--cap-drop`
still wins: if the binary's effective bit is set and it cannot get its full permitted set, `execve`
fails with `EPERM`. `--security-opt no-new-privileges` stops container processes gaining new privileges.

## Turn the audit into policy
- CI: fail Compose/stack files with `privileged: true` or `cap_add` outside an allowlist.
- Prefer `--cap-drop ALL` plus the one capability needed, and avoid `--privileged`.
- Document every capability with the reason next to the `cap_add` line.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main, `docker run` reference, security pages), Docker Engine API swagger (moby/moby master), man-pages capabilities(7), proc(5), capsh(1) and setcap(8).
- Confirmed the default capability set is the 14 entries in the `docker run` reference (AUDIT_WRITE, CHOWN, DAC_OVERRIDE, FOWNER, FSETID, KILL, MKNOD, NET_BIND_SERVICE, NET_RAW, SETFCAP, SETGID, SETPCAP, SETUID, SYS_CHROOT); the `CapEff` hex shown decodes to exactly those bits.
- Confirmed `HostConfig` fields `Privileged`, `CapAdd`, `CapDrop`, `PidMode`, `NetworkMode` in the Engine API; `capsh --decode` and `--print` in capsh(1); `security.capability` xattr, bounding-set intersection and the `EPERM` rule in capabilities(7); `CapInh/CapPrm/CapEff/CapBnd/CapAmb` in proc(5).
- Removed pscap, getpcaps, `getcap -r`, `column` and CI or runtime tool recommendations that no checked source covers.
Method: documentation only; no commands were run.
