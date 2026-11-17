---
id: computing-software.cloud-infrastructure-engineering.talos-linux.talos-reset-machine
name: talos-reset-machine
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [talosctl, reset, wipe, graceful, etcd, state-partition, kernel-args]
level: practitioner
status: docs-checked
description: "Reset a Talos node with talosctl reset: graceful versus forced, wiping only STATE and EPHEMERAL on cloud VMs, the reboot flag, and the wipe kernel argument."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/lifecycle-management/resetting-a-machine.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resetting returns a machine to its original state and is destructive: the node is removed from Kubernetes and from etcd (if applicable) and anything that normally persists across a reboot is cleared.

```sh
talosctl reset -n <node_ip_to_be_reset>
```

Flags:

```bash
Flags:
      --graceful                        if true, attempt to cordon/drain node and leave etcd (if applicable) (default true)
      --reboot                          if true, reboot the node after resetting instead of shutting down
      --system-labels-to-wipe strings   if set, just wipe selected system disk partitions by label but keep other partitions intact
```

**HA versus single node.** A graceful reset works on a member of a healthy HA cluster. On a single-node test cluster etcd cannot be left because there is only one member, so use `--graceful=false` to skip the checks that would block the reset.

**Cloud VMs.** A full reset wipes the entire disk and may leave a VM unable to boot. Unless it boots via iPXE, wipe only the STATE and EPHEMERAL partitions:

`talosctl reset --system-labels-to-wipe STATE --system-labels-to-wipe EPHEMERAL`

**Boot loops.** With console access, add the kernel parameter `talos.experimental.wipe=system` (for example through GRUB). On the next boot Talos resets the system disk and reboots. Afterwards reinstall via PXE boot or by mounting an ISO.

## Checked

Command, flag help text, graceful versus single-node guidance, cloud VM warning and the wipe kernel parameter confirmed on the Resetting a Machine page.

Method: docs-checked 2026-11-09 against the raw Resetting a Machine page (v1.15 folder), read in full.
