---
id: computing-software.systems-network-administration.icinga-2.agent-and-satellite-setup-linux-windows
name: agent-and-satellite-setup-linux-windows
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, agent, satellite, node-wizard, windows-agent, msi, accept-config, accept-commands]
level: practitioner
status: docs-checked
description: Join an Icinga 2 agent or satellite to its parent with icinga2 node wizard - parent endpoint, certificate fingerprint check, ticket, accept config and commands, zone names.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# agent and satellite setup (Linux and Windows)
**Linux.** Run `icinga2 node wizard` and answer `Y` for an agent/satellite. It asks for:
- Common name (FQDN by default) and the parent's CN.
- Whether to connect to the parent. If the node cannot reach it, answer `n`; you then copy the master's CA certificate to the node's `ca.crt` yourself and sign the CSR on the master.
- Parent endpoint host and port (5665).
- Verification of the parent certificate fingerprint, which prevents MITM; compare it with the parent's certificate fingerprint by hand.
- The CSR auto-signing ticket; blank means on-demand signing.
- Accept config from parent (needed for config sync) and accept commands (needed for command endpoint mode).
- Local zone name (defaults to the FQDN; change for a satellite) and parent zone name (default `master`; change if the parent is a satellite).
- Extra global zones, and whether to disable `conf.d` (default: disable).

The wizard enables `api`, creates the CSR and updates zones and ApiListener.

**Windows.** Requires .NET Framework 4.6 or higher (default on Windows Server 2016+) and the Universal C Runtime on Server 2012 and older. Install the Windows agent package and run its setup wizard; see the distributed monitoring chapter for the prompts.

## Checked

2026-11-04. Confirmed against the Icinga 2 distributed monitoring chapter: Linux node wizard prompts, .NET Framework 4.6 and Universal C Runtime requirements. Removed the unconfirmed openssl fingerprint command, MSI location, flavour, service user default and no-satellite claim.

Method: documentation only; no commands were run.
