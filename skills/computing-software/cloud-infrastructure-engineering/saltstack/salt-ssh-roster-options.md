---
id: computing-software.cloud-infrastructure-engineering.saltstack.salt-ssh-roster-options
name: salt-ssh-roster-options
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, salt-ssh, roster, thin-dir, pre-flight, roster-defaults, ssh-options]
level: advanced
status: docs-checked
description: "Reference the salt-ssh roster target options: host, user, port, sudo_user, priv, thin_dir, ssh_pre_flight, set_path, ssh_options, plus roster_defaults."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/ssh/roster.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Roster target options

Each target is keyed by a Salt ID. Settings: `host`, `user`, `passwd`.

Optional:
- `port`, `sudo`, `sudo_user` (must share a group with the login user or be a superuser), `tty` (when sudo needs a TTY).
- `priv`: private key path (default `salt-ssh.rsa`) or `agent-forwarding`; `priv_passwd`.
- `timeout`: seconds to establish SSH.
- `minion_opts`: dict of minion options.
- `thin_dir`: where Salt components live on the target, default `/tmp/salt-<hash>`.
- `cmd_umask`: octal umask for `salt-call`.
- `ssh_options`: list of `option=argument`.
- `set_path` (3001): PATH on the target so the expected Python is found.
- `ssh_pre_flight` (3001) and `ssh_pre_flight_args`: script run on the target before Salt commands.
- `ssh_pre_hook` (3008): script on the origin host before every run; a non-zero exit stops salt-ssh before connecting.

Pre-flight runs only when the thin directory is missing (first run or after wipe). Force it with `-w`, `ssh_run_pre_flight: True`, or `--pre-flight`.

Master config `roster_defaults` (a dict) supplies default login values for all targets.

`thin_dir` defaults to a temporary location; change it for persistent grains.

## Checked

2026-11-04: read the Salt SSH roster page in full. Confirmed every listed target option, the 3001 and 3008 version notes, the pre-flight rerun options, ssh_pre_hook failure behaviour, roster_defaults and thin_dir. Nothing removed.

Method: documentation only; no commands were run.

