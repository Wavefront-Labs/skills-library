---
id: computing-software.systems-network-administration.pi-hole.pi-hole-system-requirements
name: pi-hole-system-requirements
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-requirements, hardware-sizing, supported-os]
level: intro
status: docs-checked
description: "Check hardware, operating system, CPU architecture and addressing requirements before installing Pi-hole on a host."
sources: ["https://docs.pi-hole.net/main/prerequisites/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pi-hole system requirements

Pi-hole is light. Plan for at least 2GB free space (4GB recommended) and 512MB RAM. It is not limited to a Raspberry Pi; any hardware running a supported OS works.

**Supported operating systems** (only actively maintained versions): Alpine, Armbian OS, Debian, CentOS Stream, Fedora, Raspberry Pi OS and Ubuntu. Variants may install, but installation can fail on unsupported configurations. The init system must be systemd or sysvinit.

**Binary architectures.** The resolver binary `pihole-FTL` is pre-built for:

- x86_64 (amd64 and i686)
- armv6
- armv7
- armv8 (aarch64)
- riscv64

On any other architecture you must compile FTL from source.

**Addressing.** Pi-hole needs a static IP address to function properly. A DHCP reservation on the router is sufficient.

**Checklist before installing**

1. Confirm the OS is on the supported list and still maintained.
2. Confirm free disk space and RAM meet the minimums.
3. Confirm the CPU architecture has a pre-built `pihole-FTL`.
4. Give the host a static address or DHCP reservation.
5. Stop any other DNS server (for example BIND) that holds port 53, because Pi-hole must answer DNS itself.

## Checked

2026-11-03. Read the Prerequisites page: 2GB free space (4GB recommended), 512MB RAM, supported OS list, systemd or sysvinit, pihole-FTL architectures, static IP or DHCP reservation, and the port 53 note about BIND. Removed the reference to a ports skill by name.

Method: documentation only; no commands were run.
