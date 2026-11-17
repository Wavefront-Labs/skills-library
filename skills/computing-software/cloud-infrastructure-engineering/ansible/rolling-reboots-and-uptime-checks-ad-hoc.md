---
id: computing-software.cloud-infrastructure-engineering.ansible.rolling-reboots-and-uptime-checks-ad-hoc
name: rolling-reboots-and-uptime-checks-ad-hoc
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ad-hoc, ad-hoc-reboot, reboot-module, uptime]
level: practitioner
status: docs-checked
description: "Reboot hosts ad hoc safely with the reboot module, limit and forks for rolling batches, and check uptime and needs-restarting before and after."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/reboot_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/reboot.py", "https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html", "https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html", "https://github.com/rpm-software-management/dnf-plugins-core/blob/master/doc/needs_restarting.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rolling reboots ad hoc

## Who needs a reboot?
```bash
ansible rhel -b -m ansible.builtin.command -a 'needs-restarting -r' -o   # exit code 1 => reboot required (dnf needs-restarting --reboothint)
ansible all -m ansible.builtin.command -a 'uptime -s' -o
```

## Reboot in batches with forks and limit
```bash
ansible web -b -f 2 -m ansible.builtin.reboot -a 'reboot_timeout=900 msg="Patch reboot"'
ansible 'web[0:4]' -b -m ansible.builtin.reboot                 # slice 0:4 = web[0] through web[4] (the pattern docs show [0:2] as three hosts)
ansible web --limit @rebootlist.txt -b -m ansible.builtin.reboot
```
`-f 2` sets two forks, so at most 2 hosts are handled at a time; the `reboot` module waits for each host to come back (`reboot_timeout`, default 600 seconds) and validates with `test_command` (default `whoami`).

For health checks between batches use a playbook with `serial` and load balancer drain.

## Useful reboot args
| Arg | Use |
|---|---|
| `pre_reboot_delay` | seconds to wait before reboot; on Linux, macOS and OpenBSD it is converted to minutes and rounded down (under 60 becomes 0) |
| `post_reboot_delay` | seconds to wait after the reboot command succeeds before validating |
| `test_command` | e.g. `systemctl is-system-running` |
| `connect_timeout` | maximum seconds to wait for a successful connection before trying again |
| `boot_time_command` | command that returns a unique string for the last boot (default reads `/proc/sys/kernel/random/boot_id`) |

## Gotchas
- Prefer `ansible.builtin.reboot` over `command` with `/sbin/reboot` (the intro_adhoc docs use the latter for a simple reboot); the reboot module waits for the host to return and validates it.
- Do not include the control node or a bastion you are connecting through.
- A fork count larger than the safe batch size can take a whole tier down at once.

## Verify
- [ ] `uptime -s` on each rebooted host (via `command`) shows the new boot time.

## Checked
Checked 2026-10-26 against ansible-core devel `reboot.py`, ansible-documentation `intro_adhoc.rst` and `intro_patterns.rst`,
and dnf-plugins-core `needs_restarting.rst`. Confirmed: `reboot_timeout` 600, `test_command` default `whoami`, `pre_reboot_delay`
conversion rule, `post_reboot_delay`, `connect_timeout`, `boot_time_command` default, `-f` forks, slice semantics,
`needs-restarting -r` exit code 1. Removed unconfirmed claims: the Debian `reboot-required` file, "ad hoc has no serial" and
the reasoning that `command: reboot` always fails as unreachable.
Method: documentation only; no commands were run.
