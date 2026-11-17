---
id: computing-software.systems-network-administration.apache-guacamole.rdp-hyperv-vmconnect
name: rdp-hyperv-vmconnect
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, rdp, hyper-v, vmconnect, preconnection-pdu, preconnection-id, preconnection-blob, vm-console]
level: advanced
status: docs-checked
description: "Connect Guacamole to Hyper-V VM consoles over RDP: security=vmconnect, port 2179, preconnection-blob as VM ID, self-signed certs."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V (VMConnect) over RDP

Settings:
- `security=vmconnect`: negotiates only modes Hyper-V supports and makes the default port 2179.
- `username` and `password` of a host account allowed to open the VM.
- `preconnection-blob`: opaque string identifying the RDP source; for Hyper-V this is the destination VM's ID.
- `preconnection-id`: non-negative integer selecting a logical connection; leave blank for Hyper-V.
- `ignore-cert=true` is often needed because Hyper-V may present a self-signed certificate.

Procedure:
1. On the Hyper-V host, obtain the VM's ID, for example with PowerShell `Get-VM <VM_NAME> | Select-Object Id`.
2. Create an RDP connection to the host with the settings above.
3. Leave `port` empty (2179) unless remapped.
4. Connect.

Notes:
- The manual calls this the Preconnection PDU feature and gives no additional host-side setup; check Hyper-V documentation for enabling console access.
- `security=vmconnect` limits negotiation to protocols known to be supported by Hyper-V, so use it only for Hyper-V consoles (see apache-guacamole.rdp-network-security).

Verify: the connection shows the target VM's screen.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Guacamole manual Configuring Guacamole page: the RDP port and security mode entries and the Preconnection PDU (Hyper-V / VMConnect) section were read; other RDP sections were not. Confirmed: security vmconnect and port 2179, username and password, preconnection-blob as the destination VM ID obtained with PowerShell Get-VM, preconnection-id numeric and blank for Hyper-V, ignore-cert for self-signed certificates, and the generic nature of the preconnection PDU.
