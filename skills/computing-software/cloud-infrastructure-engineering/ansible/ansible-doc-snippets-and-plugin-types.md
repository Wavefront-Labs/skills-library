---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-doc-snippets-and-plugin-types
name: ansible-doc-snippets-and-plugin-types
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, modules-fqcn, ansible-doc, ansible-doc-snippet, plugin-types, offline-docs, keyword-docs]
level: intro
status: docs-checked
description: "Use ansible-doc offline to list modules and plugins by type, print copy-paste snippets with -s, read keyword docs, and dump JSON docs for tooling."
sources: ["https://docs.ansible.com/ansible/latest/cli/ansible-doc.html", "https://docs.ansible.com/ansible/latest/plugins/plugins.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/cli/doc.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible-doc snippets and plugin types

`ansible-doc` reads documentation from what is **installed** — exactly the versions your
playbook will use, offline. Useful on air-gapped hosts.

## Modules
```bash
ansible-doc -l                          # every module available
ansible-doc -l ansible.posix            # filter by namespace or collection name
ansible-doc -l | grep -i firewall
ansible-doc ansible.posix.firewalld     # full docs: options, notes, EXAMPLES, RETURN
ansible-doc -s ansible.posix.firewalld  # playbook snippet (only for inventory, lookup and module plugins)
ansible-doc -F | grep firewalld         # list with file paths: which file is actually used
```
In the pager, `/EXAMPLES` jumps to examples — usually the fastest way to correct syntax.

## Other plugin types: -t
```bash
ansible-doc -t lookup -l
ansible-doc -t filter -l
ansible-doc -t test -l
ansible-doc -t connection ssh           # all ssh connection options with their ansible.cfg/env/var names
ansible-doc -t become sudo
ansible-doc -t inventory amazon.aws.aws_ec2
ansible-doc -t callback -l
ansible-doc -t keyword serial           # playbook keywords and where they apply
ansible-doc -t role -l -r roles/        # roles in a path (-r/--roles-path; -e selects an entry point)
```
Types in 2.22: `become cache callback cliconf connection httpapi inventory lookup netconf shell vars
module strategy test filter role keyword`.

The config-option tables (`ini:`, `env:`, `vars:`) shown for connection/become/callback plugins
are the authoritative way to know which variable sets which option.

## Machine-readable
```bash
ansible-doc -j ansible.builtin.copy      # JSON output for one plugin
```

## Gotchas
- Only installed collections show up; set `ANSIBLE_COLLECTIONS_PATH` to point at project-local ones. `-M/--module-path` prepends a module library path, and `--playbook-dir` sets the substitute playbook directory used to resolve adjacent paths.
- `-s` output lists all options; delete what you do not need rather than leaving defaults spelled out.

## Verify
- [ ] `ansible-doc -F <module>` path points into the collection version you pinned.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in lib/ansible/cli/doc.py and constants.py (stable-2.22): `-t` choices (documentable plugin types plus role and keyword), `-l`/`-F` accept a namespace or collection filter, `-s` is limited to inventory, lookup and module, `-j`, `-r/--roles-path`, `-e/--entry-point`, `-M/--module-path`, `--playbook-dir`; `--metadata-dump` is described as internal use only.
- Removed unconfirmed claims: filter documentation version gate, ansible-navigator remarks, jq pipeline, the exam reference.

Method: documentation only; no commands were run.
