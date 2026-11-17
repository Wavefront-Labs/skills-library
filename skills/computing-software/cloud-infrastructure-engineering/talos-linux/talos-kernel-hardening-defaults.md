---
id: computing-software.cloud-infrastructure-engineering.talos-linux.talos-kernel-hardening-defaults
name: talos-kernel-hardening-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [hardening, kspp, kernel, sysctl, cmdline, cis, security-defaults]
level: practitioner
status: docs-checked
description: "What Talos hardens by default (KSPP kernel config, boot parameters, sysctls, module signing) and the talosctl commands that verify each layer on a live node."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/security/talos-default-hardening-and-cis-compliance.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/security/talos-security-checklist.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos follows the Kernel Self-Protection Project (KSPP) recommendations at four levels, with no operator configuration.

- **Build-time kernel config** (cannot be overridden by cmdline or sysctl): `CONFIG_MODULE_SIG_FORCE` enabled (all modules must be signed regardless of Secure Boot), `CONFIG_DEVMEM` not set (no `/dev/mem`), `CONFIG_KEXEC` not set (only signed `KEXEC_FILE` paths), `CONFIG_SECURITY_APPARMOR_PARANOID_LOAD` enabled, `CONFIG_TRUSTED_KEYS` not set.
- **Boot parameters**: `slab_nomerge`, `pti=on`, `init_on_alloc=1`. `init_on_free` is off for performance but can be enabled for stricter environments.
- **Runtime sysctls**: a stricter KSPP set from Talos v1.12 onwards, covering kernel pointer exposure, `/proc` access and unprivileged BPF.
- **Module and memory controls**: `module.sig_enforce=1` and `proc_mem.force_override=never` (no writing to another process's `/proc/PID/mem`).

At OS level there is no SSH, no interactive shell, an immutable root filesystem, no package manager and API-only management, so most of the CIS Distribution Independent Linux Benchmark does not apply.

Verify on a node:

```bash
talosctl get cmdline --nodes <node-ip>
talosctl get kernelparamstatus --nodes <node-ip>
talosctl get securitystate --nodes <node-ip>
talosctl services --nodes <node-ip>
talosctl get machineconfig --nodes <node-ip> -o yaml
```

The security checklist adds what stays with the operator: protect machine configs (they hold CA keys), enable disk encryption and SecureBoot with TPM, upgrade regularly with `talosctl upgrade --nodes <ip>`, apply Pod Security Admission and network policies, use the ingress firewall, limit `talosconfig` distribution, and keep off-cluster etcd snapshots.

## Checked

Hardening layers, parameter values and verification commands confirmed on the default hardening page; operator checklist items confirmed on the security checklist page.

Method: docs-checked 2026-11-09 against the raw default hardening page (read in full) and the raw security checklist page (read in full), v1.15 folder.
