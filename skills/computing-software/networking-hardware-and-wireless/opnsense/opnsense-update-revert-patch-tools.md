---
id: computing-software.networking-hardware-and-wireless.opnsense.opnsense-update-revert-patch-tools
name: opnsense-update-revert-patch-tools
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [opnsense-update, opnsense-revert, opnsense-patch, kernel-revert]
level: advanced
status: docs-checked
description: "Shell tools for OPNsense hotfixes: opnsense-update for kernel/base, opnsense-revert for packages, opnsense-patch for upstream commits."
sources: ["https://docs.opnsense.org/manual/opnsense_tools.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# opnsense-update, opnsense-revert and opnsense-patch

Three console tools handle fixes outside the normal update path. See each manpage on the system for all options.

opnsense-update fetches binary sets for combined kernel and base upgrades and package upgrades through pkg. Example from the docs: after a minor update the new kernel breaks a NIC driver. Kernels for a release are listed under the pkg.opnsense.org sets path for that version. To fall back to the release's base kernel run opnsense-update -kr 18.1 (the -k flag touches only the kernel, -r takes the version) and then opnsense-shell reboot. To return to the current kernel, run opnsense-update -k and reboot. Warning: consult the forums or open an issue before reverting a kernel; do it only on test machines or when advised by qualified team members.

opnsense-revert installs earlier versions of packages found in a release, as long as the selected mirror caches it. Example: after 18.1.5 changed strongswan and VPNs became unstable, run opnsense-revert -r 18.1.4 strongswan to keep OPNsense at 18.1.5 with the older package. Run opnsense-revert strongswan to return to the current version. To revert the whole system use opnsense-revert -r 18.1.4 opnsense, and also check whether the kernel needs a downgrade.

opnsense-patch treats each argument as an upstream git commit hash, downloads and applies them in order. Reapplying reverses a patch, and with several patches reverse the order. Example: opnsense-patch 63cfe0a to test a shaper fix. For the plugins repo use -c plugins, e.g. opnsense-patch -c plugins 699f1f2, and add -a githubusername before -c to take patches from another user's fork.

## Checked

2026-11-03. Confirmed against the OPNsense Tools manual page: the three tools, every example command and flag, the kernel revert warning. Nothing removed.

Method: documentation only; no commands were run.
