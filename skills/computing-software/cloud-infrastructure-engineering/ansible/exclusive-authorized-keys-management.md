---
id: computing-software.cloud-infrastructure-engineering.ansible.exclusive-authorized-keys-management
name: exclusive-authorized-keys-management
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, users-groups, authorized-key-exclusive, authorized-key, ssh-keys]
level: practitioner
status: docs-checked
description: "Manage authorized_keys exclusively so only declared keys remain, with key options, multiple keys per user, revocation, and safety checks against locking yourself out."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/posix/authorized_key_module.html", "https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/authorized_key.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Exclusive authorized_keys

```yaml
- name: Only the declared keys may log in as deploy
  ansible.posix.authorized_key:
    user: deploy
    key: "{{ deploy_keys | join('\n') }}"
    exclusive: true
    key_options: 'from="10.0.0.0/8",no-agent-forwarding,no-X11-forwarding'
    manage_dir: true
```

## How exclusive works
- With `exclusive: true` all other non-specified keys are removed; multiple keys go in one `key` string separated by newlines.
- The option is not loop aware: in a loop it is exclusive per iteration, so pass all keys to `key` in a single call.
- Without exclusive, removing a key requires an explicit `state: absent` task for that key.

## Keys from files or URLs
```yaml
key: "{{ lookup('ansible.builtin.file', 'files/keys/' + user + '.pub') }}"
key: https://github.com/{{ github_user }}.keys       # URL source, as in the module docs
key: file:///path/on/target/keys.pub                 # file:// prefix: searched on the remote host
```

## Revocation pattern
Keep the canonical key list in inventory (`group_vars/all/ssh_keys.yml`); offboarding = delete the line, rerun; exclusive mode removes it everywhere.

## Lockout safety
Before running exclusive on the automation account itself, assert your key is present:
```yaml
- ansible.builtin.assert:
    that: lookup('ansible.builtin.file', '~/.ssh/automation_ed25519.pub') in automation_keys | join('\n')
    fail_msg: "Refusing: controller key missing from automation_keys"
```
Run on a canary host first and keep a console/break-glass path.

## Gotchas
- `key_options` is a string of options prepended to the key in the file.
- `path:` points at an authorized_keys file other than the default `.ssh/authorized_keys` in the user's home.
- `comment` changes the comment on the key; if unset, the existing comment is kept.
- `validate_certs` (default `true`) applies when keys come from an https URL.
- `manage_dir` defaults to `true`: the module creates the directory and sets owner and permissions of an existing one; set it to `false` if `path` points to a directory it should not touch.

## Verify
- [ ] The authorized_keys file on the host contains exactly the declared keys.

## Checked
Checked 2026-10-26 against ansible.posix `plugins/modules/authorized_key.py` documentation block. Confirmed `exclusive`
behaviour and not being loop aware, `key` newline separation and URL/`file://` forms, `key_options`, `manage_dir`
default, `path`, `comment`, `state`. Removed the unconfirmed `%u` example path, the key-matching claim and the
`wc -l` check. The assert example below is a Jinja/Ansible pattern, not a module claim, and was not run.
Method: documentation only; no commands were run.
