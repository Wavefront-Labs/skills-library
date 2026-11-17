---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-navigator-modes-and-subcommands
name: ansible-navigator-modes-and-subcommands
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-navigator, navigator-mode, navigator-stdout, navigator-images, navigator-doc, navigator-collections, navigator-inventory]
level: practitioner
status: docs-checked
description: "Use ansible-navigator stdout and interactive modes and its subcommands (run, images, collections, doc, inventory, config) to inspect an execution environment."
sources: ["ansible-navigator subcommands (https://github.com/ansible/ansible-navigator/blob/main/docs/subcommands.md)", "ansible-navigator FAQ (https://github.com/ansible/ansible-navigator/blob/main/docs/faq.md)", "ansible-navigator configuration source (https://github.com/ansible/ansible-navigator/blob/main/src/ansible_navigator/configuration_subsystem/navigator_configuration.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible-navigator modes and subcommands

## Modes
- `-m stdout`: behaves like `ansible-playbook` — scrolling output, exit code; for CI and scripts.
- `-m interactive` (default): text UI for drilling into a play, task and host result and inspecting the full result without `-vvv`. Subcommands can also be entered at the prompt, for example `:run`, `:doc`, `:config`, `:inventory`, `:lint`.

```bash
ansible-navigator run site.yml -i inventories/prod -m stdout --check --diff
ansible-navigator run site.yml -m interactive        # drill down into results
```
Parameters that navigator does not use itself are passed to `ansible-playbook`, inline after the navigator parameters or after a `--` delimiter (`ansible-navigator run site.yml --forks 15`).
Password and `vars_prompt` prompts need `--enable-prompts` (stdout mode, no playbook artifact).

## Subcommands
| Subcommand | Shows |
|---|---|
| `images` | EE images available locally; select one to see details such as ansible and Python versions, collections, Python packages, OS release |
| `collections` | collections available in the selected EE |
| `doc <plugin>` | `ansible-doc` inside the EE: `ansible-navigator doc community.general.ufw -m stdout` |
| `inventory` | browse groups, hosts and vars as the EE sees them; in stdout mode it takes ansible-inventory style options such as `--graph` |
| `config` | ansible configuration as seen in the EE; in stdout mode it supports the same parameters as `ansible-config` |
| `lint` | runs ansible-lint inside the EE (image must contain it) |
| `replay <artifact.json>` | re-open a saved run in the TUI |
| `exec -- <cmd>` | run a command in the EE (also the way to run `ansible-galaxy`, `ansible-test` and `ansible-vault`) |
| `builder` | runs `ansible-builder`, which is installed with navigator |
| `settings` | review navigator settings (`--effective`, `--sources`, `--sample`, `--schema`) |
| `welcome` | start page |

Examples:
```bash
ansible-navigator images -m stdout --details ansible_collections python_packages
ansible-navigator collections -m stdout
ansible-navigator inventory -i inventories/prod -m stdout --graph
ansible-navigator config -m stdout dump --only-changed
```

## Gotchas
- Interactive mode needs a real TTY; in CI always pass `-m stdout`.
- `collections` shows the collections in the selected EE, not those installed on the host.
- `doc` without `-m stdout` opens the TUI; scripts that omit the flag will wait on it.

## Verify
- [ ] `ansible-navigator images -m stdout` lists the pinned EE image.
- [ ] CI jobs use `-m stdout` and return non-zero on failures.

## Checked
Checked 2026-10-23 against the ansible-navigator repository on GitHub (docs/subcommands.md, docs/faq.md, navigator_configuration.py): mode choices and default (`interactive`), the subcommand list (collections, config, doc, exec, images, inventory, lint, replay, run, settings, welcome, builder) and the ansible command each maps to, `--details` choices for `images`, parameter pass-through to ansible-playbook, `--enable-prompts`, and `:subcommand` prompt entry. Removed the unconfirmed numbered-screen navigation keys, the `-t lookup` example and the project `./collections` claim.
Method: documentation only; no commands were run.
