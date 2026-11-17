---
id: computing-software.cloud-infrastructure-engineering.ansible.selecting-tags-on-the-command-line
name: selecting-tags-on-the-command-line
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, tags, tags-cli, list-tags, skip-tags]
level: intro
status: docs-checked
description: "Run selected tags from the CLI: multiple tags, --tags all/tagged/untagged, combining --tags with --skip-tags, and previewing with --list-tags and --list-tasks."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html", "https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Selecting tags on the command line

```bash
ansible-playbook site.yml --tags nginx                       # only tasks tagged nginx (+ always)
ansible-playbook site.yml --tags 'nginx,certs'               # union: either tag
ansible-playbook site.yml --skip-tags slow                   # everything except slow
ansible-playbook site.yml --tags config --skip-tags restart  # skip wins over select
ansible-playbook site.yml --tags tagged                      # only tasks with at least one tag
ansible-playbook site.yml --tags untagged                    # only tasks with no tags
ansible-playbook site.yml --tags all                         # default (except never)
ansible-playbook site.yml --tags all,never                   # everything, including never-tagged tasks
```

## Preview before running
```bash
ansible-playbook site.yml --tags nginx --list-tasks
ansible-playbook site.yml --list-tags                          # every tag per play
```

## Env and config equivalents
`ANSIBLE_RUN_TAGS=nginx`, `ANSIBLE_SKIP_TAGS=slow`; in ansible.cfg `[tags]` section keys `run` and `skip` (the `TAGS_RUN` and `TAGS_SKIP` options, added in 2.5). Skip tags have precedence over run tags.

## Things that still run
- Tasks tagged `always` run unless `--skip-tags always`.
- Fact gathering carries `always` by default but is skipped if the play's own tag is skipped or not selected, and by `--skip-tags always`.
- Handlers ignore tags and run when notified by selected tasks.

## Gotchas
- Dynamic includes (`include_tasks`, `include_role`): a tag on the include applies only to the include itself. Tasks inside run only if they carry the selected tag too, or if the include uses `apply: {tags: ...}`.
- `--list-tags` and `--list-tasks` cannot show tags or tasks inside dynamically included files or roles.
- No AND logic: `--tags a,b` is a union.

## Verify
- [ ] `--list-tasks` with the intended tag selection shows exactly the expected tasks.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Tags page (playbooks_tags.rst, devel); ansible-core config/base.yml.
Confirmed:
- Five tag options, union semantics, precedence of --skip-tags, --list-tags and --list-tasks and its dynamic-include limit.
- TAGS_RUN and TAGS_SKIP options: env ANSIBLE_RUN_TAGS and ANSIBLE_SKIP_TAGS, ini [tags] run and skip, added in 2.5; skip has precedence.

Method: documentation only; no commands were run.
