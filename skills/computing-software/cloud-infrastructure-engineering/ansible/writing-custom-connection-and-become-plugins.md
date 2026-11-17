---
id: computing-software.cloud-infrastructure-engineering.ansible.writing-custom-connection-and-become-plugins
name: writing-custom-connection-and-become-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, plugin-development, custom-connection-plugin, custom-become-plugin, connectionbase, becomebase, plugin-options, privilege-escalation]
level: sme
status: docs-checked
description: "Write a custom connection plugin (ConnectionBase: exec_command, put_file, fetch_file) and a custom become plugin (BecomeBase: build_become_command, prompts) inside a collection."
sources: ["Developing plugins (https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html)", "ConnectionBase source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/connection/__init__.py)", "BecomeBase source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/become/__init__.py)", "sudo become plugin source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/become/sudo.py)", "local connection plugin source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/connection/local.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing custom connection and become plugins

Goal: reach hosts through a transport Ansible does not ship (a vendor jump API, a serial broker,
`kubectl exec`-like tooling) or escalate with an in-house tool, without forking ansible-core.
Check community.general / community.* first — `ssm`, `lxd`, `incus`, `podman`, `dzdo`, `pmrun`
and many others already exist.

## Connection plugin
`plugins/connection/vendorexec.py`:
```python
from __future__ import annotations
DOCUMENTATION = r"""
name: vendorexec
short_description: Run commands via the vendor exec API
description: [Executes commands and copies files through the vendor CLI.]
author: Platform Team
options:
  remote_addr:
    description: Target id.
    vars: [{name: inventory_hostname}, {name: ansible_host}]
  vendor_cli:
    description: Path to the CLI.
    default: vendorctl
    vars: [{name: ansible_vendorexec_cli}]
    env: [{name: VENDOREXEC_CLI}]
"""
import subprocess
from ansible.errors import AnsibleConnectionFailure
from ansible.plugins.connection import ConnectionBase

class Connection(ConnectionBase):
    transport = "acme.platform.vendorexec"
    has_pipelining = False

    def _connect(self):
        self._connected = True
        return self

    def exec_command(self, cmd, in_data=None, sudoable=True):
        super().exec_command(cmd, in_data=in_data, sudoable=sudoable)
        argv = [self.get_option("vendor_cli"), "exec", self.get_option("remote_addr"), "--", "/bin/sh", "-c", cmd]
        p = subprocess.run(argv, input=in_data, capture_output=True)
        return p.returncode, p.stdout, p.stderr      # bytes, not str

    def put_file(self, in_path, out_path):
        super().put_file(in_path, out_path)
        rc = subprocess.call([self.get_option("vendor_cli"), "cp", in_path, f"{self.get_option('remote_addr')}:{out_path}"])
        if rc != 0:
            raise AnsibleConnectionFailure(f"put_file failed: {out_path}")

    def fetch_file(self, in_path, out_path):
        super().fetch_file(in_path, out_path)
        subprocess.check_call([self.get_option("vendor_cli"), "cp", f"{self.get_option('remote_addr')}:{in_path}", out_path])

    def close(self):
        self._connected = False
```
Use with `ansible_connection: acme.platform.vendorexec`. Options declared in `DOCUMENTATION` are read with `get_option()`; the engine calls `set_options()` for connection and become plugins.

## Become plugin
`plugins/become/acmesu.py`:
```python
DOCUMENTATION = r"""
name: acmesu
short_description: Escalate with acmesu
options:
  become_user: {description: User to become, default: root, vars: [{name: ansible_become_user}]}
  become_exe: {description: Binary, default: acmesu, vars: [{name: ansible_acmesu_exe}]}
  become_pass: {description: Password, vars: [{name: ansible_become_password}], required: false}
"""
from ansible.plugins.become import BecomeBase

class BecomeModule(BecomeBase):
    name = "acme.platform.acmesu"
    fail = ("Authentication failure",)
    missing = ("Password required",)

    def build_become_command(self, cmd, shell):
        super().build_become_command(cmd, shell)
        if not cmd:
            return cmd
        self.prompt = "acmesu password:" if self.get_option("become_pass") else None
        return f"{self.get_option('become_exe')} -u {self.get_option('become_user')} -- {self._build_success_command(cmd, shell)}"
```
`_build_success_command` wraps the command so Ansible sees the success marker; `prompt` tells
the connection to answer with the password; `fail`/`missing` strings map output to clear errors.
Use with `become_method: acme.platform.acmesu`.

## Gotchas
- `exec_command` returns `(rc, stdout, stderr)` with stdout and stderr as bytes (the base class signature is `tuple[int, bytes, bytes]`).

## Verify
- [ ] `ansible-doc -t connection acme.platform.vendorexec` and `-t become acme.platform.acmesu` render.
- [ ] `ansible target -m ping -c acme.platform.vendorexec -vvvv` succeeds; `-m copy` and `-m fetch` round-trip a file; `-b --become-method acme.platform.acmesu -m command -a id` shows the target user.

## Checked

Checked 2026-10-26 against ansible-core 2.21.5 sources (devel, 2026-10-23) and ansible-documentation main (2026-10-21).
- Confirmed in `ConnectionBase`: `transport`, `has_pipelining` (default False), `_connect`, `exec_command(cmd, in_data, sudoable)` returning `tuple[int, bytes, bytes]`, `put_file`, `fetch_file`, `close`; the developer guide states the engine calls `set_options()` for become, callback, connection and shell plugins.
- Confirmed in `BecomeBase` and the sudo plugin: `name`, `fail`, `missing`, `prompt`, `build_become_command(cmd, shell)`, `_build_success_command(cmd, shell)`, `expect_prompt` requiring both a prompt and `become_pass`.
- Removed as unconfirmed: the locale, remote-tmp and FQCN-naming gotchas.

Method: documentation only; no commands were run.
