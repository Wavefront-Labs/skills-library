---
id: computing-software.cloud-infrastructure-engineering.openbao.disable-swap
name: disable-swap
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, swap, hardening, memory-swap-max, systemd]
level: practitioner
status: docs-checked
description: "Stop OpenBao secrets leaking to swap on Linux, BSD, Windows, Docker and macOS using MemorySwapMax, cgroupv2 and encrypted paging."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keeping OpenBao out of swap

Swap can leak secrets, so disable it for the process or encrypt it.

## Linux

The bundled systemd service sets `MemorySwapMax=0`. Check it:

```
systemctl cat openbao
```

Without systemd, set the cgroupv2 `memory.swap.max` to `0` for the process. Running `swapoff` system-wide is not recommended.

## Other platforms

- **BSDs:** confirm swap is encrypted, per each OS's documentation.
- **Windows:** check with `fsutil behavior query encryptpagingfile`. If it returns 0, run `fsutil behavior set encryptpagingfile 1` and reboot.
- **Docker:** run with `--memory-swappiness=0`.
- **macOS:** swap is always encrypted; nothing to do.

## Checked

2026-11-04. Confirmed against the Post-installation hardening section of the Installing OpenBao page: MemorySwapMax=0 and systemctl cat openbao, cgroupv2 memory.swap.max, swapoff not recommended, BSD encrypted swap, the Windows fsutil commands, Docker --memory-swappiness=0 and macOS. Removed the generic Verify section, which the page does not contain.

Method: documentation only; no commands were run.
