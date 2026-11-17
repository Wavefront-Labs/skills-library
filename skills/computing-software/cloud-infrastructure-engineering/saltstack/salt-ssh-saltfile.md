---
id: computing-software.cloud-infrastructure-engineering.saltstack.salt-ssh-saltfile
name: salt-ssh-saltfile
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, salt-ssh, saltfile, ssh-wipe, ssh-max-procs, ssh-log-file]
level: practitioner
status: docs-checked
description: "Set salt-ssh defaults in a Saltfile: salt-ssh key, ssh_wipe, ssh_max_procs, ssh_log_file, config_dir, and the Saltfile search order."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/ssh/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# salt-ssh Saltfile

A Saltfile is YAML keyed by tool name:

```yaml
salt-ssh:
  config_dir: path/to/config/dir
  ssh_log_file: salt-ssh.log
  ssh_max_procs: 30
  ssh_wipe: True
```

- Use the parser's destination names: `ssh_wipe`, not `wipe`.
- Search order: `--saltfile` path, `SALT_SALTFILE` environment variable, `./Saltfile`, then `~/.salt/Saltfile`.
- Saltfile values currently override command-line flags of the same name.

## Checked

2026-11-04: read the Saltfile section of the Salt SSH page in full. Confirmed the example, destination-name rule, search order and the precedence note. Nothing removed.

Method: documentation only; no commands were run.

