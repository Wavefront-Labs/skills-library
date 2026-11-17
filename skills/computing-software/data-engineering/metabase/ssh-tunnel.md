---
id: computing-software.data-engineering.metabase.ssh-tunnel
name: ssh-tunnel
category: computing-software
field: data-engineering
product: metabase
tags: [ssh-tunnel, bastion-host, allowtcpforwarding, private-network, reverse-tunnel]
level: practitioner
status: docs-checked
description: "Connect Metabase to a private database through an SSH tunnel: field mapping for host and tunnel host, key or password auth, AllowTcpForwarding, and failure modes."
sources:
  - https://www.metabase.com/docs/latest/databases/ssh-tunnel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fields for a bastion host setup:
- Toggle "Use an SSH-tunnel for database connections".
- Host and Port: the database address and port as seen from inside the network.
- SSH tunnel host and SSH tunnel port (usually 22): the bastion host as seen from outside.
- SSH tunnel username and password, or SSH authentication set to SSH Key with the private key and, if needed, a passphrase.

Localhost variant: set Host to `localhost`, use the database's local port, and set SSH tunnel host to the database server's external name.

Gotchas:
- The SSH server must have `AllowTcpForwarding` set to "yes".
- Metabase Cloud does not support VPN, so use SSH tunnelling for private networks.
- Closing the SSH connection (sleep, network change) drops all tunnelled connections.
- Tunnels are slower, add latency and may be limited by organisational policy.
- Metabase's built-in SSH client does not support Windows Domain or Kerberos authentication.
- If inbound connections are blocked, use reverse tunnelling instead.

Testing: try the credentials with a direct `ssh` command first. Allow only approved clients, including Metabase Cloud IPs on the bastion.

## Checked
2026-11-03. Confirmed against the Metabase docs page Databases, SSH tunneling: bastion and localhost field mappings, key and password authentication, direct ssh test, AllowTcpForwarding, Cloud VPN note and approved-client advice, disadvantages list, built-in SSH client limits, reverse tunnelling. Removed the unsupported failure-mode diagnosis (only the sleep or network-change drop is stated).
Method: documentation only; no commands were run.
