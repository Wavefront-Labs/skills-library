---
id: computing-software.networking-hardware-and-wireless.strongswan.linux-kernel-modules
name: linux-kernel-modules
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, kernel-modules, xfrm, config-options, ipcomp]
level: practitioner
status: docs-checked
description: "Linux kernel options and modules strongSwan needs for IPsec, including XFRM, ESP and AH, tunnel modes for kernels before 5.2, and IPComp."
sources:
  - https://docs.strongswan.org/docs/latest/install/kernelModules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# linux kernel modules
Include these kernel options:

- `CONFIG_XFRM_USER`, `CONFIG_XFRM_MIGRATE`, `CONFIG_IP_ADVANCED_ROUTER`, `CONFIG_IP_MULTIPLE_TABLES`
- `CONFIG_INET_AH`, `CONFIG_INET_ESP`, `CONFIG_INET_IPCOMP` and the `CONFIG_INET6_*` equivalents, plus `CONFIG_IPV6_MULTIPLE_TABLES`
- `CONFIG_NETFILTER`, `CONFIG_NETFILTER_XTABLES`, `CONFIG_NETFILTER_XT_MATCH_POLICY`

For kernels before 5.2, enable the IPsec modes explicitly: transport, tunnel and BEET (`CONFIG_INET_XFRM_MODE_*` and `CONFIG_INET6_XFRM_MODE_*`); newer kernels have them built in. On kernels 4.2 to 4.5, select Encrypted Chain IV Generator (`CONFIG_CRYPTO_ECHAINIV`) manually to use CBC-mode encryption.

Modules that should be loaded when a tunnel is established: `ah4 ah6 esp4 esp6 xfrm4_tunnel xfrm6_tunnel xfrm_user ip_tunnel tunnel tunnel6 xfrm4_mode_tunnel xfrm6_mode_tunnel`.

Optional: `xfrm_ipcomp` and `deflate`, needed for compression (`compress=yes`).

The page includes a shell script that greps the running kernel's config under `/boot` for the required options.

## Checked
2026-11-04. Confirmed against the Linux Kernel Modules page: required CONFIG options, the before-5.2 mode options, the kernel 4.2-4.5 echainiv note, the module name lists, and the IPComp modules. Removed the unsupported opening claim about distro kernels.

Method: documentation only; no commands were run.
