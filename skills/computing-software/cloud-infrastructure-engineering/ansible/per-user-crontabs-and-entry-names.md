---
id: computing-software.cloud-infrastructure-engineering.ansible.per-user-crontabs-and-entry-names
name: per-user-crontabs-and-entry-names
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, cron-scheduled-tasks, cron-user, cron, idempotent-cron]
level: intro
status: docs-checked
description: "Manage per-user crontab entries with the cron module: the user option, the name marker comment that makes entries idempotent, renames, and disabled entries."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/cron_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/cron.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Per-user crontabs and entry names

```yaml
- name: Nightly report for the app user
  ansible.builtin.cron:
    name: app-nightly-report          # unique per crontab
    user: app                         # whose crontab (needs become if not you)
    minute: "15"
    hour: "2"
    job: /opt/app/bin/report >> /var/log/app/report.log 2>&1
  become: true
```

## How name works
The module writes a marker comment above the line:
```
#Ansible: app-nightly-report
15 2 * * * /opt/app/bin/report >> /var/log/app/report.log 2>&1
```
Idempotence keys off that marker in the given user's crontab. Consequences:
- Changing `name` creates a **second** entry; remove the old one with `state: absent` and the old name.
- The same name in two different users' crontabs is two separate entries (fine).
- Entries added by hand (no marker comment) are not found by the module's name lookup, so it will not dedupe them.

## Disable without deleting
```yaml
- ansible.builtin.cron:
    name: app-nightly-report
    user: app
    job: /opt/app/bin/report >> /var/log/app/report.log 2>&1
    minute: "15"
    hour: "2"
    disabled: true                    # comments the line out, keeps the marker
```
Repeat the schedule fields and `job` when disabling: omitted schedule fields default to `*`.

## Remove
```yaml
- ansible.builtin.cron: {name: app-nightly-report, user: app, state: absent}
```

## Gotchas
- `cron_file` requires `user` (the account the job runs as) unless `state: absent`; relative paths resolve under `/etc/cron.d`.
- Environment variable entries use `env: true`; there `name` is the variable name, `job` is its value, and no marker comment line is added.

## Verify
- [ ] `crontab -l -u app` on the host shows the `#Ansible: app-nightly-report` marker above the entry.

## Checked
Checked 2026-10-26 against ansible-core devel `cron.py` documentation notes and code (`#Ansible: ` marker prefix, name
lookup, `disabled`, `cron_file`, `env`, defaults of `*`). Removed unconfirmed spool directory paths per distribution.
Method: documentation only; no commands were run.
