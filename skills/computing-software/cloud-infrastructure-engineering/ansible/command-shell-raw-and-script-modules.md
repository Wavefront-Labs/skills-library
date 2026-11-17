---
id: computing-software.cloud-infrastructure-engineering.ansible.command-shell-raw-and-script-modules
name: command-shell-raw-and-script-modules
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, modules-fqcn, command-vs-shell, raw-module, script-module, free-form, args-keyword, argv, creates, removes]
level: practitioner
status: docs-checked
description: "Choose between ansible.builtin command, shell, raw and script, pass free-form vs argv arguments safely, and keep them idempotent with creates, removes and changed_when."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/command_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/shell_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/raw_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/script_module.html", "https://ansible.readthedocs.io/projects/lint/rules/no-free-form/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# command vs shell vs raw vs script

First ask: is there a real module? (`ansible-doc -l | grep -i <thing>`). Only then:

| Module | Runs via | Shell features (`|`, `>`, `$VAR`, `*`) | Needs Python on target |
|---|---|---|---|
| `command` | exec, no shell | no | yes |
| `shell` | `/bin/sh -c` | yes | yes |
| `raw` | passed straight into the connection (remote shell) | yes (remote shell) | **no** |
| `script` | copies local script, runs it | inside script | no (just a shell) |

## command — the default choice
```yaml
- name: Initialise the repo
  ansible.builtin.command:
    argv: [git, init, --bare, /srv/repo.git]
    creates: /srv/repo.git/HEAD
```
`argv` avoids quoting problems (for example a value such as "user name"); give either `argv` or the free-form string, not both. `command` also expands `$VAR` references in arguments through Python (default `expand_argument_vars: true`, since 2.16; unmatched variables are left unchanged).

## shell — only when you need the shell
```yaml
- name: Count established connections
  ansible.builtin.shell: |
    set -o pipefail
    ss -tan | grep -c ESTAB
  args:
    executable: /bin/bash
  register: estab
  changed_when: false
```
`set -o pipefail` (bash) so a failing first command fails the task (ansible-lint `risky-shell-pipe`).
Quote variables: `{{ path | quote }}` — never interpolate untrusted input unquoted.

## raw — bootstrap without Python
```yaml
- hosts: new
  gather_facts: false
  tasks:
    - ansible.builtin.raw: dnf install -y python3 python3-libdnf   # the module docs' example; use your distro's package manager
      changed_when: false
```
Also for devices such as routers that have no Python, and it is supported on Windows targets. It does not support check mode, has no `creates`/`removes` and no change handler support; stdout, stderr and the return code are returned. Fact gathering needs Python, so set `gather_facts: false` when bootstrapping. The `environment` keyword only works with `raw` if `executable` is set or `become` is used.

## script — run a local script remotely
```yaml
- ansible.builtin.script: files/collect.sh --verbose
  args:
    creates: /var/tmp/collected
    executable: python3   # interpreter used to run the script
```
The `ssh` connection plugin forces a pseudo-tty (`-tt`) for `script`, so stderr is merged into stdout; use `copy` plus `command` if you need them separate. A local script path containing spaces must be quoted. `script` is supported on Windows targets.

## Free-form arguments and `args:`
Modules taking free-form input (`command`, `shell`, `raw`, `script`, `win_shell`) put options in
`args:` or alongside the `cmd:` key:
```yaml
- ansible.builtin.command:
    cmd: make install
    chdir: /opt/src
    creates: /usr/local/bin/tool
```
Inline `key=value` (`command: make chdir=/opt/src`) still works but ansible-lint flags free-form syntax (`no-free-form`). Prefer the dict form.

## Idempotence
- `creates:` / `removes:` skip the task when a path (or glob, for `command`) exists / is missing; `creates` is evaluated before `removes`.
- `changed_when: false` for read-only commands; `changed_when: "'Updated' in r.stdout"` otherwise.
- `failed_when: r.rc not in [0, 3]` for tools with non-zero success codes.

## Gotchas
- `command` with `>` or `|` passes them as literal args — silent wrong behaviour.
- `shell` runs `/bin/sh` on the remote node: bashisms need `executable` set to an absolute path such as `/bin/bash`.
- None of these support diff mode. In check mode `command`, `shell` and `script` only report a correct status when `creates` or `removes` is given; otherwise `command` returns `changed=False` without running. `raw` does not support check mode. `check_mode: false` forces a read-only task to run.
- For Windows targets use `win_command` or `win_shell` instead of `command`/`shell`.

## Verify
- [ ] ansible-lint clean (`command-instead-of-module`, `command-instead-of-shell`, `no-changed-when`).
- [ ] Second run reports `changed=0` for these tasks.

## Checked
Checked 2026-10-25 against the ansible-core devel module documentation for command, shell, raw and script (lib/ansible/modules, commit of 2026-10) and the ansible-lint `no-free-form` and `risky-shell-pipe` rule pages. Confirmed: no-shell behaviour of `command`, `argv` and `expand_argument_vars` (2.16), `creates`/`removes` semantics and ordering, `shell` using `/bin/sh` with `executable`, `raw` no check mode and no Python need, the `script` pseudo-tty note, `quote` filter advice, and the lint rule names. Removed unconfirmed claims about the shlex split, dash on Debian, `$HOME` under become, and the python3 package-existence one-liner.
Method: documentation only; no commands were run.
