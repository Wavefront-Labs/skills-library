---
id: computing-software.cloud-infrastructure-engineering.saltstack.salt-ssh-roster-basics
name: salt-ssh-roster-basics
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, salt-ssh, roster, agentless, raw-command]
level: intro
status: docs-checked
description: "Run Salt agentless with salt-ssh: the default /etc/salt/roster file, short and full roster entries, running commands and states, and limits."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/ssh/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# salt-ssh and the roster

Salt SSH uses plain SSH instead of ZeroMQ and needs no remote agent; it is slower than standard Salt and production ready since 2014.7.0. Python must exist on the target unless you use `-r` for raw commands.

Roster default: `/etc/salt/roster`.

```yaml
web1:
  host: 192.168.42.1
  user: fred
  passwd: foobarbaz
  sudo: True
web2:
  host: 192.168.42.2
```

The basic form maps a Salt ID straight to an address (`web1: 192.168.42.1`).

Omit `passwd` to use keys.

Run:

```
salt-ssh '*' test.version
salt-ssh '*' -r 'ifconfig'
```

- Only glob and regex targeting are supported.
- States work by replacing `salt` with `salt-ssh`; the run compiles on the master and referenced `salt://` files travel in the same tarball.
- Grains set through salt-ssh are not persisted across reboots by default (see the roster `thin_dir` option).

## Checked

2026-11-04: read the Salt SSH page in full. Confirmed the ZeroMQ and agent comparison, 2014.7.0 production readiness, Python requirement and -r, the default roster path and examples, glob and regex only targeting, states via salt-ssh and the grains persistence note. Nothing removed.

Method: documentation only; no commands were run.

