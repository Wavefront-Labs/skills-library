---
id: computing-software.devops-ci-cd.rundeck.bastion-host-node-executor
name: bastion-host-node-executor
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, bastion-host, openssh-bastion, proxycommand, dry-run]
level: advanced
status: docs-checked
description: "Reach nodes through a jump host with the OpenSSH Bastion Host node executor and file copier: properties, ssh_config example and dry-run preview."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/projects/node-execution/bastionssh.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The plugin provides a node executor and file copier that run ssh through a bastion host, for servers reachable only via a jump host.

Properties:
- Bastion SSH Key Storage Path: identity for the bastion connection.
- SSH Options: extra options for the ssh command.
- ssh_config: ProxyCommand and other flags (see `ssh_config(5)`).
- Dry run?: print the command that would run without executing it.

Per node, set the `ssh-key-storage-path` attribute to the key in Key Storage to use for the target node.

Configure as the project's default node executor and file copier on the Simple Configuration tab, or in `project.properties`:

```properties
project.plugin.NodeExecutor.openssh-bastion-host.node-executor.ssh_config=Host * \
  StrictHostKeyChecking no
  Port 22
  ProxyCommand ssh user@bastionhost -W %h\:%p
  IdentityFile @plugin.config.identity_file@
project.plugin.NodeExecutor.openssh-bastion-host.node-executor.ssh_options="-q -oClearAllForwardings=yes"
```

Multiple lines use a trailing backslash plus an indent on the next line.

Verify with Dry run first: the log prints the generated ssh_config and the ssh or scp command line.

The plugin repo `openssh-bastion-node-execution` has a Docker example (`./start-docker-example.sh`, then port 8080, admin/admin) where Rundeck can only reach the nodes via the bastion.

## Checked

2026-11-04. Confirmed against the Rundeck docs page OpenSSH Bastion Host Node Execution Plugins: the four properties, the ssh-key-storage-path node attribute, the project.properties example keys, the trailing backslash multi-line rule, dry run behaviour, and the Docker example (start-docker-example.sh, port 8080, admin/admin). Nothing removed.

Method: documentation only; no commands were run.
