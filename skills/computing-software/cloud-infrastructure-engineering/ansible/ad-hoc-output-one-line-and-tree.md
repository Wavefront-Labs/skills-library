---
id: computing-software.cloud-infrastructure-engineering.ansible.ad-hoc-output-one-line-and-tree
name: ad-hoc-output-one-line-and-tree
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ad-hoc, ad-hoc-one-line, ad-hoc-forks, ad-hoc-tree]
level: intro
status: docs-checked
description: "Shape ad hoc output across many hosts: -o one-line mode, -f forks, --tree per-host JSON files, and grepping results for audits."
sources: ["https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html", "https://docs.ansible.com/ansible/latest/cli/ansible.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/callback/oneline.py", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/callback/tree.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ad hoc output: one-line, forks and --tree

## One line per host
```bash
ansible all -m ansible.builtin.command -a 'uptime' -o
# web01 | CHANGED | rc=0 | (stdout)  10:02:11 up 41 days, ...
ansible all -m ansible.builtin.ping -o | grep -v SUCCESS      # only problem hosts
```
`-o` (`--one-line`) selects the `oneline` stdout callback, which condenses each result to one line. That callback is
deprecated in ansible-core 2.22 (removal scheduled for 2.23); for new tooling prefer the `default` callback with
`result_format` (env `ANSIBLE_CALLBACK_RESULT_FORMAT`, `json` or `yaml`).

## Forks
```bash
ansible all -m ansible.builtin.shell -a 'rpm -q openssl' -f 50 -o
```
Default forks is 5 (`forks` in `[defaults]`, env `ANSIBLE_FORKS`). Raise for read-only audits on hundreds of hosts; keep low for changes.

## --tree: one JSON file per host
```bash
ansible all -m ansible.builtin.setup -a 'filter=ansible_distribution*' --tree /tmp/facts
ls /tmp/facts            # web01  web02  db01 ...
cat /tmp/facts/web01     # the JSON result for that host
```
`--tree` uses the `tree` callback, which can also be enabled for playbooks (`callbacks_enabled = tree`, directory from
`ANSIBLE_CALLBACK_TREE_DIR`, default `~/.ansible/tree`). The `tree` callback is deprecated in ansible-core 2.22 and
scheduled for removal in 2.23.

## Audit recipes
```bash
ansible all -b -m ansible.builtin.shell -a "grep -c '^PermitRootLogin no' /etc/ssh/sshd_config" -o | grep -v 'rc=0'
ansible all -m ansible.builtin.command -a 'cat /etc/os-release' --tree out/ -o > /dev/null
```

## Gotchas
- Unreachable hosts also produce tree files with `"unreachable": true`.

## Verify
- [ ] Count of tree files equals `ansible all --list-hosts | tail -n +2 | wc -l`.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in plugins/callback/oneline.py and tree.py: both deprecated, removed_in 2.23; `-o` is the oneline callback, `--tree` sets the tree directory (option `directory`, env ANSIBLE_CALLBACK_TREE_DIR, default ~/.ansible/tree); tree writes a file on ok, failed and unreachable results.
- Confirmed in config/base.yml: DEFAULT_FORKS default 5, env ANSIBLE_FORKS; and in doc_fragments/result_format_callback.py: option result_format, env ANSIBLE_CALLBACK_RESULT_FORMAT.
- Removed unconfirmed claims: per-fork memory figure, jq pipelines, the always-CHANGED remark.

Method: documentation only; no commands were run.
