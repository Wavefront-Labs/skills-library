---
id: computing-software.systems-network-administration.linux.nvme-over-fabrics-tcp-initiator
name: nvme-over-fabrics-tcp-initiator
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nvme-of, nvme-tcp, nvme-cli, nvme-discover, native-nvme-multipath, san, storage-networking]
level: advanced
status: docs-checked
description: "Connect a Linux host to NVMe/TCP storage with nvme-cli: hostnqn, discover and connect, persistent connections with discovery.conf/nvmf-autoconnect, and native NVMe multipath."
sources:
  - https://github.com/linux-nvme/nvme-cli
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_storage_devices/configuring-nvme-over-fabrics-using-nvme-tcp_managing-storage-devices
  - https://nvmexpress.org/specifications/
  - https://github.com/linux-nvme/nvme-cli/blob/master/Documentation/nvme-fabrics.conf.txt
  - https://github.com/linux-nvme/nvme-cli/blob/master/Documentation/CONFIGURATION.md
  - https://docs.kernel.org/admin-guide/nvme-multipath.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NVMe over Fabrics (NVMe/TCP) initiator

## Prereqs
```bash
dnf install nvme-cli      # apt install nvme-cli
modprobe nvme-tcp && echo nvme-tcp > /etc/modules-load.d/nvme-tcp.conf
cat /etc/nvme/hostnqn     # nqn.2014-08.org.nvmexpress:uuid:...  (give this to the storage admin for host mapping)
nvme gen-hostnqn > /etc/nvme/hostnqn   # if missing; the host NQN must be unique per host (check cloned images)
```
## Discover and connect
```bash
nvme discover -t tcp -a 192.0.2.50 -s 8009
nvme connect -t tcp -a 192.0.2.50 -s 4420 -n nqn.2010-06.com.vendor:array1:subsys1
nvme connect-all -t tcp -a 192.0.2.50 -s 8009        # everything the discovery controller offers
nvme list ; nvme list-subsys                          # namespaces appear as /dev/nvmeXnY
```
## Persist across reboots
nvme-cli 3.x reads `/etc/nvme/nvme-fabrics.conf` (plus `/etc/nvme/nvme-fabrics.conf.d/*.conf`), an INI file; `nvme connect-all` and `nvme discover` use it by default:
```ini
[Discovery Controller]
controller = transport=tcp;traddr=192.0.2.50;trsvcid=8009
controller = transport=tcp;traddr=198.51.100.50;trsvcid=8009   # second path
```
```bash
nvme config-convert                       # one-time conversion of legacy /etc/nvme/discovery.conf or config.json
systemctl enable nvmf-autoconnect.service # runs: nvme connect-all --owner=autoconnect
```
Network-backed filesystems in fstab need `_netdev` (and `nofail` if the system should boot without them).

## Multipath
Native NVMe multipath merges namespaces with the same identifier into one block device; paths follow ANA (an optimized path is preferred over a non-optimized one).
```bash
nvme list-subsys                                   # shows each controller path and its state
cat /sys/module/nvme_core/parameters/iopolicy      # numa (default) | round-robin | queue-depth
echo -n round-robin > /sys/module/nvme_core/parameters/iopolicy   # or nvme_core.iopolicy=round-robin on the kernel command line
```
Don't layer dm-multipath on top unless the vendor requires it.

## Gotchas
- Duplicate host NQN / host ID on cloned VMs makes hosts indistinguishable to the storage array.
- `--ctrl-loss-tmo` is the maximum time in seconds to retry reconnecting after controller loss.

## Verify
- [ ] `nvme list-subsys` shows all paths `live`; reboot reconnects automatically; pulling one path keeps I/O flowing.

## Checked

Checked against the nvme-cli v3.1 sources (released 2026-09-18: `Documentation/nvme-fabrics.conf.txt`, `CONFIGURATION.md`, `nvme-connect-all`, `nvme-gen-hostnqn`, `fabrics-options`, `nvmf-autoconnect.service.in`) and the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (admin-guide/nvme-multipath) on 2026-10-26. Confirmed: default host identity files `/etc/nvme/hostnqn` and `hostid`, `nvme gen-hostnqn`, `/etc/nvme/nvme-fabrics.conf` and its `.d` drop-ins with `[Discovery Controller]` and `controller = transport=...;traddr=...;trsvcid=...` syntax, `nvme config-convert` for legacy discovery.conf/config.json, `nvmf-autoconnect.service` running `nvme connect-all --owner=autoconnect`, `--ctrl-loss-tmo` meaning, multipath policies numa (default), round-robin, queue-depth set through the `nvme_core` `iopolicy` parameter, ANA preference, `_netdev` and `nofail` in systemd.mount. Found stale: the old plain-text `/etc/nvme/discovery.conf` format is no longer read directly by current nvme-cli. Removed: ctrl_loss_tmo default, the per-subsystem iopolicy path, the `nvme_core` multipath parameter read, RHEL default claim, MTU claim.

Method: documentation only; no commands were run.
