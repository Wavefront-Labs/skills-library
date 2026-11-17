---
id: computing-software.cybersecurity-defensive.falco.kernel-events-architecture
name: kernel-events-architecture
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [libscap, drivers, api-version, schema-version, scap-open]
level: advanced
status: docs-checked
description: "Understand how libscap negotiates API and schema versions with Falco kernel drivers, the event header, and the scap-open debugging tool."
sources:
  - https://falco.org/docs/concepts/event-sources/kernel/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Falco libraries component `libscap` gathers syscall data and talks to the kernel drivers. The kernel module is installed and deployed separately as a kernel object; the modern eBPF probe can be installed directly by libscap.

On connecting, libscap negotiates two versions with the driver, expressed as a semver subset:
- API version: the communication mechanism between kernel and userspace. The kernel module may use `ioctl`s and a ring buffer; the modern eBPF probe uses maps and different APIs depending on kernel version.
- Schema version: which events the driver supports. It changes whenever the list of supported syscall events changes.

Check what your binary needs with `falco --version`. The output includes Falco, libraries, plugin API and rules engine versions, and under `Driver` the minimum API and schema versions plus the default driver version. These describe the binary's requirements, not a separately installed kernel module.

Each event has a header (`ts` in nanoseconds since epoch, `tid`, `len`, `type`, `nparams`) followed by an array of parameter lengths and then the parameters. For `dup3` the encoding has four parameters.

Debug with `scap-open`, an example tool in the falcosecurity/libs repository that dumps raw events from various drivers.

Gotcha: libscap verifies at startup that a separately deployed driver is compatible, so a driver/Falco version mismatch shows up at start-up rather than in rules; compare `falco --version` with the driver you installed.

## Checked

2026-11-08. Read the Kernel Events Architecture page in full. Softened the version-mismatch gotcha to what the page states.

Method: documentation only; no commands were run.
