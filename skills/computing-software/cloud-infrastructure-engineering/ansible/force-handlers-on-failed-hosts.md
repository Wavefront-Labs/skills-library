---
id: computing-software.cloud-infrastructure-engineering.ansible.force-handlers-on-failed-hosts
name: force-handlers-on-failed-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, handlers, force-handlers, error-handling, failed-hosts]
level: practitioner
status: docs-checked
description: "Make notified handlers still run when a later task fails using --force-handlers, the force_handlers play keyword or config, and know the cases where they still do not run."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html#handlers-and-failure", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Forcing handlers on failed hosts

Default: Ansible runs handlers at the end of each play section. If a task notifies a handler but
another task fails later in the play, the handler does not run on that host by default, which may
leave the host in an unexpected state. For example, a task changes a configuration file and notifies a
handler to restart the service; if a later task fails, the file is changed but the service is not restarted.

## Turn it on
```bash
ansible-playbook site.yml --force-handlers
```
```yaml
- hosts: web
  force_handlers: true
```
```ini
[defaults]
force_handlers = True        # ANSIBLE_FORCE_HANDLERS
```
When handlers are forced, Ansible runs all notified handlers on all hosts, even hosts with failed tasks.
The setting can be given per play, on the command line, or in configuration (`DEFAULT_FORCE_HANDLERS`, default false).

## Where it can still fail
- Certain errors can still prevent a handler from running, for example a host becoming unreachable.
- `any_errors_fatal` ends the play on all hosts after the fatal task; see the error-handling docs
  before relying on handlers in that case.

## Alternative patterns
- Validate before changing: for example `template` with `validate: 'nginx -t -c %s'` so a bad config never lands.
- A `block` with a `rescue` section that runs `meta: flush_handlers`: the documented way to make
  sure all handlers run even if an error occurs.

## Gotchas
- Forcing a restart after a half-applied change can turn a failed run into an outage; decide per play.
- The recap still reports the host as failed.

## Verify
- [ ] Inject a failure (`ansible.builtin.fail`) after the notifying task in a test run: with `force_handlers` the handler runs for that host.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_error_handling.rst "Handlers and failure",
playbooks_blocks.rst) and the ansible-core `DEFAULT_FORCE_HANDLERS` config entry. Confirmed option names, env var,
ini key, default false. Removed unconfirmed claims about handler-failure ordering, `serial` batch behaviour and the checksum-comparison pattern.
Method: documentation only; no commands were run.
