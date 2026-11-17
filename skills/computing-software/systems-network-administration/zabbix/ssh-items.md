---
id: computing-software.systems-network-administration.zabbix.ssh-items
name: ssh-items
category: computing-software
field: systems-network-administration
product: zabbix
tags: [ssh, ssh-run, libssh, sshkeylocation, agentless, key]
level: practitioner
status: docs-checked
description: "Run commands on devices over SSH with ssh.run items, using password or public key authentication."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/ssh_checks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SSH checks are agentless: the server (or proxy) opens an SSH session and runs a command. The server must be built with libssh or libssh2; from RHEL 8 only libssh is supported, and libssh is recommended elsewhere.

Item fields:
- Type: SSH agent.
- Key: ssh.run[unique short description,<ip>,<port>,<encoding>,<ssh options>,<subsystem>]. The description is required and must be unique per host. The default port is 22, not the port of the host interface.
- Authentication method: Password or Public key.
- User name, and Password or key file names with passphrase.
- Executed script: shell commands; the return value is limited to 16 MB, and libssh2 may truncate scripts to about 32 kB.

Key-file authentication needs one server change. In zabbix_server.conf uncomment and set SSHKeyLocation to the directory holding the public and private keys, then restart the server. Generate the pair as the zabbix user, for example sudo -u zabbix ssh-keygen -t rsa with an empty passphrase if the item does not supply one. Package installs often give the zabbix account a different home directory such as /var/lib/zabbix, so either point SSHKeyLocation there or move the home directory with usermod -m -d after stopping the zabbix processes. Keep the home directory mode at 700.

For public key authentication, give the user name plus the public and private key file names (defaults id_rsa.pub and id_rsa); the passphrase field stays empty if none was set.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/itemtypes/ssh_checks): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
