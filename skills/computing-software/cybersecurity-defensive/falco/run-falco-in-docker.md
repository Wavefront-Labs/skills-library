---
id: computing-software.cybersecurity-defensive.falco.run-falco-in-docker
name: run-falco-in-docker
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [docker-run, modern-ebpf, least-privilege, cap-sys-admin, tracefs]
level: practitioner
status: docs-checked
description: "Run Falco in a container with the modern eBPF driver at least privilege, with the capability list, mounts and tracefs path caveats."
sources:
  - https://falco.org/docs/setup/container/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Falco in a container reads kernel events by default. Least privilege is recommended over `--privileged`. Modern eBPF, least privileged:

```shell
docker run --rm -it \
           --cap-drop all \
           --cap-add sys_admin \
           --cap-add sys_resource \
           --cap-add sys_ptrace \
           -v /sys/kernel/tracing:/sys/kernel/tracing:ro \
           -v /var/run/docker.sock:/host/var/run/docker.sock \
           -v /proc:/host/proc:ro \
           -v /etc:/host/etc:ro \
           falcosecurity/falco:<version>
```

The true minimum capabilities are `CAP_SYS_PTRACE`, `CAP_SYS_RESOURCE`, `CAP_BPF` and `CAP_PERFMON`; the command uses `CAP_SYS_ADMIN` because Docker does not yet support `CAP_BPF` and `CAP_PERFMON`.

The fully privileged form replaces the capabilities with `--privileged`, keeping the same mounts.

Gotchas:
- If tracefs lives at `/sys/kernel/debug/tracing`, mount that path onto `/sys/kernel/tracing` inside the container.
- Mounting tracefs is optional but recommended; dropping it reduces access but loses TOCTOU mitigation support.
- Kernel module users first install the driver on the host with the `falcosecurity/falco-driver-loader` image, then run Falco with `-e HOST_ROOT=/`, `--cap-add SYS_PTRACE --pid=host` and one `--device /dev/falcoX` per CPU.
- The kernel-module `--device` form needs `-e HOST_ROOT=/` because devices cannot be remapped to `/host/dev`; run Falco itself with `falco -o engine.kind=kmod`. Modern eBPF is bundled in the binary and needs no driver install.
- Configure with `-o` flags or by mounting a custom `falco.yaml`; set `SKIP_DRIVER_LOADER` to skip the falcoctl driver step on start when the driver is already installed.
- With AppArmor enabled (for example Ubuntu), add `--security-opt apparmor:unconfined`; check with `docker info | grep -i apparmor`.

## Checked

2026-11-08. Read the cited container setup page in full. Added the kernel-module form notes (HOST_ROOT, falco -o engine.kind=kmod), SKIP_DRIVER_LOADER and the config options, all as documented on the page.

Method: documentation only; no commands were run.
