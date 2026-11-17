---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-faq-troubleshooting
name: tetragon-faq-troubleshooting
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [faq-startup, tetragon, btf, kernel-lockdown, macos]
level: practitioner
status: docs-checked
description: "Fix Tetragon start failures from missing BTF or Kernel Lockdown, and run it on a Mac or standalone using the project FAQ."
sources:
  - "https://tetragon.io/docs/installation/faq/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon start-up troubleshooting

## Missing BTF file
Symptom: logs say `BTF discovery: default kernel btf file does not exist` for `/sys/kernel/btf/vmlinux`, then fatal `Failed to start tetragon` with advice to use `--btf` and/or `--kernel`.

Why: Tetragon needs BTF (BPF Type Format) to load programs using CO-RE (Compile Once, Run Everywhere), which patches struct field offsets to the running kernel. Most common distributions ship `CONFIG_DEBUG_INFO_BTF=y`. By default Tetragon looks at `/sys/kernel/btf/vmlinux`; it also looks for the vmlinux file in `/var/lib/tetragon/btf`.

If the kernel has no BTF:
- Retrieve the BTF file for your kernel version from an external source.
- Build it from kernel debug symbols (needs pahole and LLVM).
- Rebuild the kernel with `CONFIG_DEBUG_INFO_BTF=y`.

Point Tetragon at a file with `--btf`.

## Standalone (outside Kubernetes)
Yes. Use the Container or Package installation guides, or build with `make` and run `sudo ./tetragon --bpf-lib bpf/objs`.

## Mac
Run a Linux virtual machine (examples listed: Lima, UTM, VirtualBox with arm64 in developer preview) using a recent distribution that ships BTF. Docker Desktop must be recent (for example 24.0.6 with kernel 6.4.16-linuxkit) since older VMs lacked BTF. Check:

```shell
docker run -it --rm --privileged --pid=host ubuntu nsenter -t 1 -m -u -n -i sh -c 'cat /proc/config.gz | gunzip | grep CONFIG_DEBUG_INFO_BTF'
docker run -it --rm --privileged --pid=host ubuntu nsenter -t 1 -m -u -n -i sh -c 'ls -la /sys/kernel/btf/vmlinux'
```
Expect `CONFIG_DEBUG_INFO_BTF=y`, `CONFIG_DEBUG_INFO_BTF_MODULES=y` and the vmlinux file present.

## "operation not permitted" (Kernel Lockdown)
Lockdown has `integrity` and `confidentiality` modes. In `confidentiality` mode Tetragon fails with `EPERM` loading BPF programs; use `integrity`. Startup logs warn and show `Lockdown=confidentiality`. Check with:

```shell
cat /sys/kernel/security/lockdown
```

## Checked

Date: 2026-11-07

FAQ page read in full. Reworded the BTF search order to match the page (vmlinux first, and it also looks in /var/lib/tetragon/btf).

Method: documentation only; no commands were run.
