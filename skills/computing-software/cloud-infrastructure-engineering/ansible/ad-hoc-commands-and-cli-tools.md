---
id: computing-software.cloud-infrastructure-engineering.ansible.ad-hoc-commands-and-cli-tools
name: ad-hoc-commands-and-cli-tools
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ad-hoc, adhoc, ansible-cli, ansible-doc, ansible-console, ansible-inventory, ansible-config, ansible-pull, one-liners, command-module, shell-module, setup-module, fleet-queries, ansible-galaxy, ansible-vault, ansible-playbook, ansible-test]
level: practitioner
status: docs-checked
description: "Use the Ansible CLI family for one-off work: ad hoc ansible commands for fleet queries and fixes, ansible-doc to find modules, ansible-inventory to debug groups, ansible-console, ansible-pull."
sources: ["https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html", "https://docs.ansible.com/ansible/latest/cli/ansible.html", "https://docs.ansible.com/ansible/latest/cli/ansible-doc.html", "https://docs.ansible.com/ansible/latest/cli/ansible-inventory.html", "https://docs.ansible.com/ansible/latest/cli/ansible-console.html", "https://docs.ansible.com/ansible/latest/cli/ansible-pull.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ad hoc commands and the CLI tool family

**Goal:** answer "what is on these hosts" and "fix this one thing everywhere" in one
line, without writing a playbook, and know which CLI tool to reach for.

## 1. `ansible` ad hoc
```bash
ansible <pattern> -m <module> -a '<args>' [-i inv] [-b] [-l subset] [-f 50] [-o] [-C]
ansible all -m ansible.builtin.ping -o                       # reachability, one line per host
ansible web -m ansible.builtin.setup -a 'filter=ansible_distribution*'
ansible all -m ansible.builtin.command -a 'uptime'           # default module is command
ansible all -m ansible.builtin.shell -a 'ss -ltnp | grep :443'  # needs a shell for the pipe
ansible db -b -m ansible.builtin.service -a 'name=postgresql state=restarted'
ansible all -b -m ansible.builtin.package -a 'name=vim state=present' -C   # check mode
ansible all -m ansible.builtin.copy -a 'src=./motd dest=/etc/motd mode=0644' -b
ansible all -m ansible.builtin.fetch -a 'src=/var/log/messages dest=./logs/ flat=no'
ansible all -m ansible.builtin.debug -a "msg={{ ansible_host }} {{ inventory_hostname }}"
```
Useful flags: `-o` one-line output and `-t ./out` tree output (one JSON file per host). In
ansible-core 2.22 the `oneline` and `tree` callbacks behind those two flags are marked deprecated, with
removal scheduled for 2.23, so do not build long-lived tooling on either. Also `-B 3600 -P 0`
async/background, `-e key=val`, `-k`/`-K` for SSH/sudo passwords, `--list-hosts` to preview the
pattern without running anything.

`command` is not processed through a shell, so `|`, `>`, `;` and `&` do not work (and unmatched `$VAR`
references are left unchanged); use `shell` only when you need those. Prefer purpose-built modules for convergence.

## 2. `ansible-doc`
```bash
ansible-doc -l | grep -i firewall            # list modules matching
ansible-doc ansible.posix.firewalld          # full docs with examples
ansible-doc -s ansible.builtin.lineinfile    # snippet: args only
ansible-doc -t lookup -l ; ansible-doc -t filter community.general.json_query
ansible-doc -t connection ssh
ansible-doc -j ansible.builtin.copy                          # JSON output for one plugin
```
Plugin types accepted by `ansible-doc -t` in 2.22: `module` (default), `become`, `cache`, `callback`,
`cliconf`, `connection`, `filter`, `httpapi`, `inventory`, `lookup`, `netconf`, `shell`, `strategy`,
`test`, `vars`, plus `role` (shows argument_specs) and `keyword`. `-s` (snippet) works only for
`inventory`, `lookup` and `module`.

## 3. `ansible-inventory`
```bash
ansible-inventory --graph                    # tree of groups and hosts
ansible-inventory --graph web --vars         # with resolved variables
ansible-inventory --host db01                # merged vars for one host (JSON)
ansible-inventory --list --yaml > snapshot.yml   # freeze a dynamic inventory
ansible-inventory --list --export            # minimal form, good for diffs
```
This is the fastest way to prove whether a host is in a group or where a variable value came from.

## 4. `ansible-console`
Interactive REPL with the same semantics as ad hoc: `ansible-console web`, then
`cd db`, `forks 20`, `become true`, `setup filter=ansible_memtotal_mb`, `list`. Good for incident work against a saved subset.

## 5. `ansible-pull`
Inverts the model: the node clones a repo and runs `local.yml` against itself.
```bash
ansible-pull -U https://git.example.com/infra/config.git -C main -d /var/lib/ansible/local -i localhost, local.yml
```
Put it in a systemd timer for self-healing fleets with no control node (edge, autoscaled
instances). `-o` only runs when the repo changed; `--purge` removes the checkout after.

## 6. The rest of the family
`ansible-playbook` (runs), `ansible-galaxy` (roles/collections), `ansible-vault`
(secrets), `ansible-config` (`list`, `dump --only-changed`, `init`, `validate`), `ansible-lint`, `ansible-test`
(collection CI), `ansible-navigator` (EE-aware TUI), `ansible-builder` (EE images).

## Gotchas
- Ad hoc runs have no play, so there is no `vars_files` or role. For anything needing a variable file, write a playbook.
- Quoting: wrap `-a` in single quotes; inside, `key=value` pairs or a JSON dict (`-a '{"name":"nginx","state":"started"}'`) when values contain spaces.
- `ansible all -m shell -a 'rm -rf /tmp/x'` on 500 hosts with `-f 5` takes 100 batches; raise `-f`.
- `ansible-doc` only sees collections on `collections_path`.

## Verify
- [ ] `ansible all -m ping -o | grep -vc SUCCESS` is 0 for the target inventory.
- [ ] `ansible-inventory --host X` shows the expected `ansible_host` and group vars before running anything destructive.
- [ ] `ansible-doc -s <module>` works for every FQCN you intend to use (collection is installed and on path).

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in lib/ansible/cli (adhoc options, doc.py, pull.py, inventory.py, console.py) and option_helpers.py: flags `-o`, `-t/--tree`, `-B`, `-P`, `-f`, `--list-hosts`; ansible-pull `-U -C -d -o --purge`; ansible-inventory `--export`, `--yaml`; ansible-console `cd`, `forks`, `become`, `list`; ansible-doc `-t` choices, `-s` limited to three types, `-j`, `-F`, `-l`.
- Confirmed in plugins/callback/oneline.py and tree.py that both are marked deprecated with removed_in 2.23.
- Confirmed in modules/command.py that command output is not passed through a shell.
- Removed unconfirmed claims: the metadata-dump recipe (ansible-doc marks it internal use only), console tab completion, `ansible-galaxy collection list` tip, the RHCE objectives source.

Method: documentation only; no commands were run.
