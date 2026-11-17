---
id: computing-software.networking-hardware-and-wireless.arista-eos.linux-bash
name: linux-bash
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, bash, eos-linux, fastcli, shell]
level: practitioner
status: draft
description: "Drop into the EOS bash shell, run FastCli, and use Linux tools carefully on the switch."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bash shell and Linux underneath EOS
Goal: use the Linux layer for diagnostics and scripting.

```
switch# bash
[admin@switch ~]$ uname -a
[admin@switch ~]$ FastCli -p15 -c "show version"
[admin@switch ~]$ tcpdump -ni et1 -c 10
[admin@switch ~]$ ip netns list
```

```
switch# bash timeout 30 ls /mnt/flash
```

- Kernel interfaces appear as `et1`, `ma1`; VRFs appear as network namespaces `ns-<vrf>`.
- Persistent files live in `/mnt/flash`; the rest resets on reload.
- `sudo` is available to privileged roles; `FastCli` is the CLI from shell.
- Running tcpdump on the CPU path shows only traffic punted to the CPU, not hardware-forwarded flows (use `monitor session` for those).

Gotcha: do not edit system files or install packages outside the supported extension mechanism (`.swix`). Changes outside `/mnt/flash` vanish, and misuse can affect the control plane.

Operational tip: keep shell use for diagnostics; configuration belongs in the CLI so it is saved, reviewed and replicated. Use `bash -c` one-liners in scripts with explicit timeouts.

## Verify
- `bash uname -a` returns the Linux kernel; `bash FastCli -p15 -c "show version"` matches the CLI output.
