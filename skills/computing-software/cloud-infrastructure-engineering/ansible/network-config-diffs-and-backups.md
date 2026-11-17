---
id: computing-software.cloud-infrastructure-engineering.ansible.network-config-diffs-and-backups
name: network-config-diffs-and-backups
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, network-automation, config-diff, network-diff, diff-against, config-backup, rendered-state]
level: practitioner
status: docs-checked
description: "See and control network config changes: --check --diff with resource modules, diff_against running/startup/intended in ios_config, backups, and rendered/parsed states."
sources: ["https://github.com/ansible-collections/cisco.ios/blob/main/plugins/modules/ios_config.py", "https://github.com/ansible-collections/cisco.ios/blob/main/plugins/modules/ios_vlans.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/network_resource_modules.rst", "https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/modules/cli_config.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network config diffs and backups

## Resource modules: before / commands / after
```yaml
- cisco.ios.ios_vlans:
    config: "{{ vlans }}"
    state: merged
  register: r
- ansible.builtin.debug: {var: r.commands}     # exact CLI that was (or would be) sent
```
Return keys: `before` (structured state before), `commands`, `after`. With `--check` they report the
commands that would be sent without applying them.

Offline planning (no device needed):
```yaml
- cisco.ios.ios_vlans:
    config: "{{ vlans }}"
    state: rendered            # → r.rendered: list of CLI lines
- cisco.ios.ios_vlans:
    running_config: "{{ lookup('file', 'show_vlan.txt') }}"
    state: parsed              # text → structured data
```

## ios_config: compare whole configs
```yaml
- name: Compare running config to intended
  cisco.ios.ios_config:
    diff_against: intended
    intended_config: "{{ lookup('template', 'sw.cfg.j2') }}"
    diff_ignore_lines: ['ntp clock-period .*', '! Last configuration change.*']
  check_mode: true

- name: Unsaved changes?
  cisco.ios.ios_config:
    diff_against: startup       # running vs startup
  check_mode: true
  register: unsaved
```
Run with `--diff` to print the differences. `diff_against: running` shows what a task's lines would change.

## Backups before change
```yaml
- cisco.ios.ios_config:
    backup: true
    backup_options:
      dir_path: "backups/{{ inventory_hostname }}"
      filename: "{{ inventory_hostname }}.cfg"
```
Platform-agnostic: `ansible.netcommon.cli_config` (`backup: true`, `diff_match`, `rollback`,
`commit_comment`); support for the last two depends on the platform's cliconf plugin.

## Gotchas
- Volatile lines (timestamps, crypto keys, NTP clock period) cause permanent diffs — add `diff_ignore_lines`.
- `ios_config` `lines` with `match: line` compares individual lines; indentation and parents must match device output (`parents:`).
- Resource modules ignore unmanaged attributes with `merged`, remove them with `replaced` (per resource item) and `overridden` (whole resource). Review `commands` for `no ...` lines before applying overridden.

## Verify
- [ ] `--check --diff` on a compliant device: `changed=0`, no diff.
- [ ] Backup file exists and is non-empty for every device changed.

## Checked

Checked 2026-10-26 against the cisco.ios and ansible.netcommon collection sources (main) and the Ansible network resource module page. Confirmed: `ios_config` `diff_against` choices running, startup and intended with `intended_config`, `diff_ignore_lines`, `backup` with `backup_options` `dir_path` and `filename`; resource module states merged, replaced, overridden, rendered (offline, `rendered` key) and parsed (`running_config` option, `parsed` key); `before`, `commands` and `after` results; `cli_config` options `backup`, `rollback`, `commit_comment` and `diff_match`. Removed the `now()` filename template and the claim that `--diff` prints before/after for resource modules, which no page confirms.

Method: documentation only; no commands were run.
